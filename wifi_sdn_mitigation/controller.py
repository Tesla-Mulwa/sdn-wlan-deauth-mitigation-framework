import time
import random
from threading import Lock, Event
import config
from network import AccessPoint, Client

class Controller:
    def __init__(self, aps, clients, attack_target, run_id, blocked_runs):
        self.aps = {}
        for ap_name, ap_cfg in aps.items() if isinstance(aps, dict) else ((ap, {}) for ap in aps):
            if isinstance(ap_cfg, dict):
                self.aps[ap_name] = AccessPoint(ap_name, ap_cfg.get("capacity", 10), ap_cfg.get("restore_eff", 0.9))
            else:
                self.aps[ap_name] = AccessPoint(ap_name)
        
        self.clients = {}
        for name, cfg in clients.items():
            self.clients[name] = Client(
                name, cfg["ip"], cfg["ap"], cfg.get("backup"),
                cfg.get("stability", 1.0), cfg.get("restore_chance", 0.9)
            )
        
        self.attack_target = attack_target
        self.run_id = run_id
        self.deauth_events = []
        self.attack_blocked = run_id in blocked_runs
        self.attack_detected = False
        self.detection_time = None
        self.block_time = None
        self.reroute_times = {}
        self.restore_times = {}
        self.attack_start_time = None
        self.attack_end_time = None
        self.lock = Lock()
        self.stop_event = Event()
        self.attack_active = Event()
        self.disconnected_clients = set()

    def inject_deauth(self, target_ap):
        with self.lock:
            self.deauth_events.append(time.time())
            for client in self.clients.values():
                if (client.current_ap == target_ap and 
                    client.connected and 
                    random.random() < config.DISCONNECT_PROBABILITY):
                    client.disconnect()
                    self.disconnected_clients.add(client.name)
                    print(f"Client {client.name} disconnected from {target_ap}")

    def run_monitor(self):
        print(f"Monitoring started (Run {self.run_id})...")
        while not self.stop_event.is_set():
            self.monitor_step()
            time.sleep(config.MONITOR_SLEEP)
        print(f"Monitoring stopped (Run {self.run_id})")

    def monitor_step(self):
        now = time.time()
        
        if not self.attack_detected and self.attack_start_time:
            self.attack_detected = True
            self.detection_time = now
            print(f"Attack detected on {self.attack_target} at {self.detection_time}")
            
            if self.attack_blocked:
                self.block_time = now
                print(f"Attacker blocked at {self.block_time}")
        
        if not self.attack_blocked:
            for client_name, client in self.clients.items():
                if (now - client.last_ping_time > config.DISCONNECT_THRESHOLD and 
                   client.connected and client.current_ap == self.attack_target):
                    client.disconnect()
                    self.disconnected_clients.add(client_name)
                    print(f"Client {client_name} disconnected due to ping timeout")
                
                # Handle rerouting with retries
                if (not client.connected and client.current_ap == self.attack_target and
                    (client.reroute_retries < config.MAX_REROUTE_RETRIES) and
                    (now - client.last_reroute_attempt > config.REROUTE_RETRY_DELAY or client.last_reroute_attempt == 0)):
                    self.reroute_client(client_name)
            
            if (self.attack_end_time or 
               (self.attack_start_time and 
                now - self.attack_start_time > config.ATTACK_DURATION)):
                self.restore_clients()
                if not self.attack_end_time:
                    self.attack_end_time = now
                    print(f"Attack ended on {self.attack_target} at {self.attack_end_time}")
                    self.attack_active.clear()

    def reroute_client(self, client_name):
        client = self.clients[client_name]
        if client.connected:
            return False

        client.last_reroute_attempt = time.time()
        client.reroute_retries += 1
        
        # Try backup APs first (ordered by preference)
        if client.backup:
            for backup_ap in client.backup:
                ap = self.aps.get(backup_ap)
                if ap and ap.add_client(client):
                    success = self.attempt_reroute(client, backup_ap)
                    if success:
                        return True
        
        # Fallback to least-loaded AP if all backups fail
        least_loaded_ap = self.find_least_loaded_ap(exclude_ap=client.current_ap)
        if least_loaded_ap:
            return self.attempt_reroute(client, least_loaded_ap)
        
        print(f"Reroute failed for {client_name} after {client.reroute_attempts} attempts")
        return False

    def attempt_reroute(self, client, target_ap):
        ap = self.aps[target_ap]
        load_factor = ap.get_load_factor()
        success_chance = (client.stability * config.BASE_REROUTE_SUCCESS * 
                        (1 - load_factor))
        
        if random.random() < success_chance:
            self.aps[client.current_ap].remove_client(client)
            client.reconnect(target_ap)
            ap.add_client(client)
            self.reroute_times[client.name] = time.time()
            print(f"Client {client.name} rerouted to {target_ap}")
            return True
        return False

    def find_least_loaded_ap(self, exclude_ap=None):
        least_loaded = None
        min_load = float('inf')
        
        for ap_name, ap in self.aps.items():
            if ap_name == exclude_ap:
                continue
            load = ap.get_load_factor()
            if load < min_load and len(ap.clients) < ap.capacity:
                min_load = load
                least_loaded = ap_name
        return least_loaded

    def restore_clients(self):
        now = time.time()
        for client_name, client in self.clients.items():
            if client.rerouted and client.connected:
                last_event = max([t for t in self.deauth_events if t < now] + [0])
                if (now - last_event >= config.RESTORE_WAIT and 
                   now - self.attack_end_time >= config.RESTORE_WAIT):
                    client.restore_attempts += 1
                    ap = self.aps[client.original_ap]
                    load_factor = ap.get_load_factor()
                    restore_chance = (client.restore_chance * config.BASE_RESTORE_SUCCESS * 
                                    ap.restore_eff * (1 - load_factor))
                    
                    if random.random() < restore_chance:
                        self.aps[client.current_ap].remove_client(client)
                        client.reconnect(client.original_ap)
                        self.aps[client.original_ap].add_client(client)
                        self.restore_times[client_name] = now
                        print(f"Client {client_name} restored to {client.original_ap}")

    def stop(self):
        self.stop_event.set()
        for client in self.clients.values():
            client.should_stop = True