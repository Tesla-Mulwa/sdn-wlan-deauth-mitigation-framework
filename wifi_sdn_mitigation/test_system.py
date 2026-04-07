#!/usr/bin/env python3
"""
Test script for WiFi SDN Mitigation Simulation
Verifies all components work correctly together
"""

import os
import sys
import time
import random

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import config
        print("✓ config.py imported successfully")
    except Exception as e:
        print(f"✗ config.py import failed: {e}")
        return False
    
    try:
        from simulator import run_simulation
        print("✓ simulator.py imported successfully")
    except Exception as e:
        print(f"✗ simulator.py import failed: {e}")
        return False
    
    try:
        from controller import Controller
        print("✓ controller.py imported successfully")
    except Exception as e:
        print(f"✗ controller.py import failed: {e}")
        return False
    
    try:
        from network import Client, AccessPoint, Attacker
        print("✓ network.py imported successfully")
    except Exception as e:
        print(f"✗ network.py import failed: {e}")
        return False
    
    try:
        from metrics import log_metrics
        print("✓ metrics.py imported successfully")
    except Exception as e:
        print(f"✗ metrics.py import failed: {e}")
        return False
    
    try:
        from visualization import NetworkVisualizer
        print("✓ visualization.py imported successfully")
    except Exception as e:
        print(f"✗ visualization.py import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas imported successfully")
    except Exception as e:
        print(f"✗ pandas import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib imported successfully")
    except Exception as e:
        print(f"✗ matplotlib import failed: {e}")
        return False
    
    try:
        import seaborn as sns
        print("✓ seaborn imported successfully")
    except Exception as e:
        print(f"✗ seaborn import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration generation"""
    print("\nTesting configuration...")
    
    try:
        import config
        
        # Test that scenarios are generated
        if not config.SCENARIOS:
            print("✗ No scenarios generated")
            return False
        
        print(f"✓ Generated {len(config.SCENARIOS)} scenarios")
        
        # Test each scenario
        for scenario_id, scenario_config in config.SCENARIOS.items():
            print(f"  Testing {scenario_id}...")
            
            # Check required keys
            required_keys = ['clients', 'aps', 'attack_target', 'expected_attacked_clients']
            for key in required_keys:
                if key not in scenario_config:
                    print(f"    ✗ Missing key: {key}")
                    return False
            
            # Check clients
            clients = scenario_config['clients']
            if not clients:
                print(f"    ✗ No clients in {scenario_id}")
                return False
            
            print(f"    ✓ {len(clients)} clients configured")
            
            # Check APs
            aps = scenario_config['aps']
            if isinstance(aps, dict):
                print(f"    ✓ {len(aps)} APs with capacity config")
            else:
                print(f"    ✓ {len(aps)} APs configured")
            
            # Check spatial config
            if hasattr(config, 'SPATIAL_CONFIG'):
                print(f"    ✓ Spatial configuration available")
            
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_simulation():
    """Test a single simulation run"""
    print("\nTesting simulation...")
    
    try:
        import config
        from simulator import run_simulation
        
        # Get first scenario
        scenario_id = list(config.SCENARIOS.keys())[0]
        scenario_config = config.SCENARIOS[scenario_id]
        
        print(f"Running test simulation for {scenario_id}...")
        
        # Run simulation
        start_time = time.time()
        metrics = run_simulation(scenario_id, 1, {1})  # Run 1, blocked
        end_time = time.time()
        
        if metrics is None:
            print("✗ Simulation returned None")
            return False
        
        print(f"✓ Simulation completed in {end_time - start_time:.2f} seconds")
        
        # Check metrics
        required_metrics = [
            'run', 'attack_blocked', 'num_attacked_clients',
            'num_disconnected', 'num_rerouted', 'num_restored',
            'mitigation_latency_ms', 'rerouting_latency_ms', 'restoration_latency_ms',
            'rerouting_success_rate', 'restoration_success_rate',
            'packet_loss_rate', 'throughput', 'throughput_percentage'
        ]
        
        for metric in required_metrics:
            if metric not in metrics:
                print(f"✗ Missing metric: {metric}")
                return False
        
        print("✓ All required metrics present")
        print(f"  Attack blocked: {metrics['attack_blocked']}")
        print(f"  Attacked clients: {metrics['num_attacked_clients']}")
        print(f"  Throughput: {metrics['throughput']:.1f} Mbps")
        
        return True
        
    except Exception as e:
        print(f"✗ Simulation test failed: {e}")
        return False

def test_visualization():
    """Test visualization generation"""
    print("\nTesting visualization...")
    
    try:
        import config
        from visualization import NetworkVisualizer
        
        # Create visualizer
        visualizer = NetworkVisualizer(save_plots=False, show_plots=False)
        print("✓ Visualizer created")
        
        # Test spatial layout generation
        scenario_id = list(config.SCENARIOS.keys())[0]
        scenario_config = config.SCENARIOS[scenario_id]
        
        # This should not fail even without data
        visualizer.plot_spatial_layout(scenario_id, scenario_config)
        print("✓ Spatial layout generation successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Visualization test failed: {e}")
        return False

def test_gui_import():
    """Test GUI import (without launching)"""
    print("\nTesting GUI import...")
    
    try:
        from gui import WiFiSDNGUI
        print("✓ GUI module imported successfully")
        return True
    except Exception as e:
        print(f"✗ GUI import failed: {e}")
        print("  Note: GUI requires tkinter which may not be available in all environments")
        return False

def main():
    """Run all tests"""
    print("WiFi SDN Mitigation Simulation - System Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Simulation Test", test_simulation),
        ("Visualization Test", test_visualization),
        ("GUI Import Test", test_gui_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                print(f"✓ {test_name} PASSED")
                passed += 1
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nYou can now run:")
        print("  python main.py                    # Interactive mode")
        print("  python main.py --gui              # GUI mode")
        print("  python main.py --scenario 'S1 (3 APs/Dynamic)' --runs 10")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("  pip install -r requirements.txt   # Install dependencies")
        print("  python -c 'import tkinter'        # Check tkinter availability")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 