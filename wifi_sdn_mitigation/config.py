import random
import math

# Spatial layout configuration
SPATIAL_CONFIG = {
    "network_radius": 100,  # meters
    "ap_positions": {
        "AP1": {"x": 0, "y": 0},
        "AP2": {"x": 50, "y": 0},
        "AP3": {"x": 25, "y": 43.3},
        "AP4": {"x": -25, "y": 43.3},
        "AP5": {"x": -50, "y": 0},
        "AP6": {"x": -25, "y": -43.3},
        "AP7": {"x": 25, "y": -43.3}
    }
}

def generate_dynamic_scenarios():
    """Generate scenarios with dynamic client allocation (20-30 clients per AP)"""
    scenarios = {}
    
    # Scenario 1: Variable APs (1-10), 60-90 clients total
    num_aps = random.randint(1, 10)
    ap_clients = {f"AP{i}": random.randint(20, 30) for i in range(1, num_aps + 1)}
    num_attackers = random.randint(1, 10)
    
    clients_s1 = {}
    client_id = 1
    
    # Generate clients for each AP
    for ap_name, num_clients in ap_clients.items():
        backup_aps = [f"AP{i}" for i in range(1, num_aps + 1) if f"AP{i}" != ap_name]
        for i in range(num_clients):
            clients_s1[f"client{client_id}"] = {
                "ip": f"10.0.0.{client_id}",
                "ap": ap_name,
                "backup": backup_aps,
                "stability": random.uniform(0.7, 0.95),
                "restore_chance": random.uniform(0.75, 0.95)
            }
            client_id += 1
    
    # Randomly select attack target
    attack_target = f"AP{random.randint(1, num_aps)}"
    
    scenarios[f"S1 ({num_aps} APs/Dynamic)"] = {
        "clients": clients_s1,
        "aps": {ap_name: {"capacity": max(num_clients, 15), "restore_eff": random.uniform(0.8, 0.95)} 
                for ap_name, num_clients in ap_clients.items()},
        "attack_target": attack_target,
        "expected_attacked_clients": ap_clients[attack_target],
        "num_attackers": num_attackers,
        "num_aps": len(ap_clients)
    }
    
    # Scenario 2: Variable APs (1-10), 100-300 clients total
    num_aps = random.randint(1, 10)
    ap_clients = {f"AP{i}": random.randint(20, 30) for i in range(1, num_aps + 1)}
    num_attackers = random.randint(1, 10)
    
    clients_s2 = {}
    client_id = 1
    
    # Generate clients for each AP
    for ap_name, num_clients in ap_clients.items():
        backup_aps = [f"AP{i}" for i in range(1, num_aps + 1) if f"AP{i}" != ap_name]
        for i in range(num_clients):
            clients_s2[f"client{client_id}"] = {
                "ip": f"10.0.1.{client_id}",
                "ap": ap_name,
                "backup": backup_aps,
                "stability": random.uniform(0.7, 0.95),
                "restore_chance": random.uniform(0.75, 0.95)
            }
            client_id += 1
    
    # Randomly select attack target
    attack_target = f"AP{random.randint(1, num_aps)}"
    
    scenarios[f"S2 ({num_aps} APs/Dynamic)"] = {
        "clients": clients_s2,
        "aps": {ap_name: {"capacity": max(num_clients, 20), "restore_eff": random.uniform(0.8, 0.95)} 
                for ap_name, num_clients in ap_clients.items()},
        "attack_target": attack_target,
        "expected_attacked_clients": ap_clients[attack_target],
        "num_attackers": num_attackers,
        "num_aps": len(ap_clients)
    }
    
    # Scenario 3: Variable APs (1-10), 140-300 clients total
    num_aps = random.randint(1, 10)
    ap_clients = {f"AP{i}": random.randint(20, 30) for i in range(1, num_aps + 1)}
    num_attackers = random.randint(1, 10)
    
    clients_s3 = {}
    client_id = 1
    
    for ap_name, num_clients in ap_clients.items():
        backup_aps = [f"AP{i}" for i in range(1, num_aps + 1) if f"AP{i}" != ap_name]
        for i in range(num_clients):
            clients_s3[f"client{client_id}"] = {
                "ip": f"10.0.2.{client_id}",
                "ap": ap_name,
                "backup": backup_aps,
                "stability": random.uniform(0.7, 0.95),
                "restore_chance": random.uniform(0.75, 0.95)
            }
            client_id += 1
    
    # Randomly select attack target
    attack_target = f"AP{random.randint(1, num_aps)}"
    
    scenarios[f"S3 ({num_aps} APs/Dynamic)"] = {
        "clients": clients_s3,
        "aps": {ap_name: {"capacity": max(num_clients, 25), "restore_eff": random.uniform(0.8, 0.95)} 
                for ap_name, num_clients in ap_clients.items()},
        "attack_target": attack_target,
        "expected_attacked_clients": ap_clients[attack_target],
        "num_attackers": num_attackers,
        "num_aps": len(ap_clients)
    }
    
    return scenarios

# Generate dynamic scenarios
SCENARIOS = generate_dynamic_scenarios()

# Legacy scenarios (keeping for backward compatibility)
LEGACY_SCENARIOS = {
    "S1 (3 APs/10 clients)": {
        "clients": {
            "client1": {"ip": "10.0.0.1", "ap": "AP1", "backup": ["AP2", "AP3"]},
            "client2": {"ip": "10.0.0.2", "ap": "AP1", "backup": ["AP2", "AP3"]},
            "client3": {"ip": "10.0.0.3", "ap": "AP1", "backup": ["AP2", "AP3"]},
            "client4": {"ip": "10.0.0.4", "ap": "AP1", "backup": ["AP2", "AP3"]},
            "client5": {"ip": "10.0.0.5", "ap": "AP2", "backup": ["AP1", "AP3"]},
            "client6": {"ip": "10.0.0.6", "ap": "AP2", "backup": ["AP1", "AP3"]},
            "client7": {"ip": "10.0.0.7", "ap": "AP2", "backup": ["AP1", "AP3"]},
            "client8": {"ip": "10.0.0.8", "ap": "AP3", "backup": ["AP1", "AP2"]},
            "client9": {"ip": "10.0.0.9", "ap": "AP3", "backup": ["AP1", "AP2"]},
            "client10": {"ip": "10.0.0.10", "ap": "AP3", "backup": ["AP1", "AP2"]},
        },
        "aps": ["AP1", "AP2", "AP3"],
        "attack_target": "AP1",
        "expected_attacked_clients": 4
    },
    "S2 (5 APs/15 clients)": {
        "clients": {
            "client1": {"ip": "10.0.1.1", "ap": "AP1", "backup": ["AP2", "AP3", "AP4"], "stability": 0.8, "restore_chance": 0.85},
            "client2": {"ip": "10.0.1.2", "ap": "AP1", "backup": ["AP2", "AP3", "AP4"], "stability": 0.7, "restore_chance": 0.75},
            "client3": {"ip": "10.0.1.3", "ap": "AP1", "backup": ["AP2", "AP3", "AP4"], "stability": 0.9, "restore_chance": 0.95},
            "client4": {"ip": "10.0.1.4", "ap": "AP1", "backup": ["AP2", "AP3", "AP4"], "stability": 0.6, "restore_chance": 0.65},
            "client5": {"ip": "10.0.1.5", "ap": "AP2", "backup": ["AP1", "AP4", "AP3"], "stability": 0.85, "restore_chance": 0.9},
            "client6": {"ip": "10.0.1.6", "ap": "AP2", "backup": ["AP1", "AP4", "AP3"], "stability": 0.75, "restore_chance": 0.8},
            "client7": {"ip": "10.0.1.7", "ap": "AP2", "backup": ["AP1", "AP4", "AP3"], "stability": 0.8, "restore_chance": 0.85},
            "client8": {"ip": "10.0.1.8", "ap": "AP3", "backup": ["AP1", "AP2", "AP4", "AP5"], "stability": 0.7, "restore_chance": 0.75},
            "client9": {"ip": "10.0.1.9", "ap": "AP3", "backup": ["AP1", "AP2", "AP4", "AP5"], "stability": 0.9, "restore_chance": 0.95},
            "client10": {"ip": "10.0.1.10", "ap": "AP3", "backup": ["AP1", "AP2", "AP4", "AP5"], "stability": 0.6, "restore_chance": 0.65},
            "client11": {"ip": "10.0.1.11", "ap": "AP4", "backup": ["AP2", "AP3", "AP5", "AP1"], "stability": 0.8, "restore_chance": 0.85},
            "client12": {"ip": "10.0.1.12", "ap": "AP4", "backup": ["AP2", "AP3", "AP5", "AP1"], "stability": 0.7, "restore_chance": 0.75},
            "client13": {"ip": "10.0.1.13", "ap": "AP4", "backup": ["AP2", "AP3", "AP5", "AP1"], "stability": 0.85, "restore_chance": 0.9},
            "client14": {"ip": "10.0.1.14", "ap": "AP5", "backup": ["AP3", "AP4", "AP2"], "stability": 0.9, "restore_chance": 0.95},
            "client15": {"ip": "10.0.1.15", "ap": "AP5", "backup": ["AP3", "AP4", "AP2"], "stability": 0.75, "restore_chance": 0.8},
        },
        "aps": {
            "AP1": {"capacity": 8, "restore_eff": 0.9},
            "AP2": {"capacity": 8, "restore_eff": 0.85},
            "AP3": {"capacity": 10, "restore_eff": 0.8},
            "AP4": {"capacity": 8, "restore_eff": 0.9},
            "AP5": {"capacity": 6, "restore_eff": 0.85}
        },
        "attack_target": "AP3",
        "expected_attacked_clients": 3
    },
    "S3 (7 APs/50 clients)": {
        "clients": {
            **{f"client{i}": {"ip": f"10.0.2.{i}", "ap": f"AP{(i-1)//7 + 1}", "backup": [f"AP{j}" for j in range(1,8) if j != (i-1)//7 + 1]} 
               for i in range(1, 41)},
            "client41": {"ip": "10.0.2.41", "ap": "AP5", "backup": ["AP1", "AP2", "AP3", "AP4", "AP6", "AP7"]},
            "client42": {"ip": "10.0.2.42", "ap": "AP5", "backup": ["AP1", "AP2", "AP3", "AP4", "AP6", "AP7"]},
            "client43": {"ip": "10.0.2.43", "ap": "AP5", "backup": ["AP1", "AP2", "AP3", "AP4", "AP6", "AP7"]},
            "client44": {"ip": "10.0.2.44", "ap": "AP5", "backup": ["AP1", "AP2", "AP3", "AP4", "AP6", "AP7"]},
            "client45": {"ip": "10.0.2.45", "ap": "AP5", "backup": ["AP1", "AP2", "AP3", "AP4", "AP6", "AP7"]},
            **{f"client{i}": {"ip": f"10.0.2.{i}", "ap": "AP6", "backup": ["AP5", "AP7", "AP1", "AP2", "AP3", "AP4"]} for i in range(46, 48)},
            **{f"client{i}": {"ip": f"10.0.2.{i}", "ap": "AP7", "backup": ["AP5", "AP6", "AP1", "AP2", "AP3", "AP4"]} for i in range(48, 51)},
        },
        "aps": ["AP1", "AP2", "AP3", "AP4", "AP5", "AP6", "AP7"],
        "attack_target": "AP5",
        "expected_attacked_clients": 12
    }
}

# System constants
DETECTION_PROBABILITY = 1.0
ATTACK_FPS = 50
ATTACK_DURATION = 5
PING_INTERVAL = 0.1
DISCONNECT_THRESHOLD = 0.2
RESTORE_WAIT = 0.5
BASE_THROUGHPUT = 25
MAX_THROUGHPUT_DEVIATION = 7  # Maximum downward deviation in Mbps
MONITOR_SLEEP = 0.05
BASE_REROUTE_SUCCESS = 0.8
BASE_RESTORE_SUCCESS = 0.85
DISCONNECT_PROBABILITY = 1.0
REROUTE_RETRY_DELAY = 0.2  # 200ms between retries
MAX_REROUTE_RETRIES = 3     # Maximum number of reroute attempts

# Visualization settings
VISUALIZATION_CONFIG = {
    "save_plots": True,
    "show_plots": False,
    "plot_format": "png",
    "plot_dpi": 300,
    "figure_size": (12, 8),
    "color_palette": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]
}