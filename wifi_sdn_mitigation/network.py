import time
import random
from threading import Lock, Event
import config

class Client:
    def __init__(self, name, ip, current_ap, backup_ap, stability=1.0, restore_chance=0.9):
        self.name = name
        self.ip = ip
        self.current_ap = current_ap
        self.original_ap = current_ap
        self.backup = backup_ap or []
        self.connected = True
        self.rerouted = False
        self.pings_sent = 0
        self.pings_dropped = 0
        self.last_ping_time = time.time()
        self.should_stop = False
        self.stability = stability
        self.restore_chance = restore_chance
        self.reroute_attempts = 0
        self.restore_attempts = 0
        self.reroute_retries = 0
        self.last_reroute_attempt = 0
        self.lock = Lock()

    def run_ping(self):
        while not self.should_stop:
            with self.lock:
                self.pings_sent += 1
                self.last_ping_time = time.time()
                if not self.connected and random.random() < 0.05:
                    self.pings_dropped += 1
            time.sleep(config.PING_INTERVAL)

    def reconnect(self, ap):
        with self.lock:
            self.current_ap = ap
            self.connected = True
            self.rerouted = ap != self.original_ap
            if self.rerouted:
                self.reroute_retries = 0  # Reset retry counter on successful reroute

    def disconnect(self):
        with self.lock:
            self.connected = False
            self.reroute_retries = 0  # Reset retry counter on new disconnection

class AccessPoint:
    def __init__(self, name, capacity=10, restore_eff=0.9):
        self.name = name
        self.capacity = capacity
        self.restore_eff = restore_eff
        self.clients = []
        self.lock = Lock()

    def add_client(self, client):
        with self.lock:
            if client not in self.clients and len(self.clients) < self.capacity:
                self.clients.append(client)
                return True
        return False

    def remove_client(self, client):
        with self.lock:
            if client in self.clients:
                self.clients.remove(client)

    def get_load_factor(self):
        with self.lock:
            return len(self.clients) / self.capacity

class Attacker:
    def __init__(self, target_ap):
        self.target_ap = target_ap
        self.should_stop = False

    def start_attack(self, duration, controller):
        start_time = time.time()
        while (time.time() - start_time < duration and 
              not controller.stop_event.is_set() and
              not self.should_stop and
              controller.attack_active.is_set()):
            if not controller.attack_blocked:
                controller.inject_deauth(self.target_ap)
            time.sleep(1.0 / config.ATTACK_FPS)