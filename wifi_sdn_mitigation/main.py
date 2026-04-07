import os
import sys
import time
import random
import argparse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulator import run_simulation
from visualization import NetworkVisualizer
import config

def display_scenario_menu():
    print("\nAvailable Scenarios:")
    for i, scenario_id in enumerate(config.SCENARIOS.keys(), 1):
        print(f"{i}. {scenario_id}")
    print("0. Run all scenarios")
    print("G. Launch GUI")
    print("Q. Quit")

def get_user_choice():
    while True:
        choice = input("\nSelect scenario to run (number), G for GUI, or Q to quit: ").strip().upper()
        if choice == 'Q':
            return 'Q'
        if choice == 'G':
            return 'GUI'
        if choice == '0':
            return 'ALL'
        if choice.isdigit() and 1 <= int(choice) <= len(config.SCENARIOS):
            return list(config.SCENARIOS.keys())[int(choice)-1]
        print("Invalid selection. Please try again.")

def generate_blocked_runs(num_runs=20):
    """Generate exactly 50% blocked and 50% unblocked runs in random order"""
    # Ensure exactly 50% blocked (10 out of 20)
    num_blocked = num_runs // 2
    blocked = [1] * num_blocked + [0] * (num_runs - num_blocked)
    random.shuffle(blocked)
    return {i+1 for i, val in enumerate(blocked) if val == 1}

def run_selected_scenario(scenario_id, num_runs=20, generate_plots=True):
    print(f"\n=== Running {scenario_id} ===")
    print(f"Configuration: {num_runs} runs, 50% blocked (randomly distributed)")
    
    successful_runs = 0
    blocked_runs = generate_blocked_runs(num_runs)
    
    # Initialize visualizer
    visualizer = NetworkVisualizer(save_plots=generate_plots, show_plots=False)
    
    for run_id in range(1, num_runs + 1):
        is_blocked = run_id in blocked_runs
        print(f"\nRun {run_id}/{num_runs} (Blocked: {is_blocked})")
        try:
            metrics = run_simulation(scenario_id, run_id, blocked_runs)
            if metrics:
                successful_runs += 1
                print(f"Run {run_id} completed successfully")
            else:
                print(f"Run {run_id} failed")
        except Exception as e:
            print(f"Run failed: {str(e)}")
    
    # Generate plots if requested
    if generate_plots and successful_runs > 0:
        print(f"\nGenerating plots for {scenario_id}...")
        try:
            visualizer.generate_all_plots(scenario_id)
            print("Plots generated successfully!")
        except Exception as e:
            print(f"Error generating plots: {str(e)}")
    
    return successful_runs

def launch_gui():
    """Launch the GUI application"""
    try:
        from gui import main as gui_main
        print("Launching GUI...")
        gui_main()
    except ImportError as e:
        print(f"Error launching GUI: {str(e)}")
        print("Make sure all required dependencies are installed:")
        print("pip install matplotlib seaborn pandas tkinter")
    except Exception as e:
        print(f"Error launching GUI: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='WiFi SDN Mitigation Simulation')
    parser.add_argument('--gui', action='store_true', help='Launch GUI mode')
    parser.add_argument('--scenario', type=str, help='Scenario to run')
    parser.add_argument('--runs', type=int, default=20, help='Number of runs')
    parser.add_argument('--no-plots', action='store_true', help='Disable plot generation')
    
    args = parser.parse_args()
    
    if args.gui:
        launch_gui()
        return
    
    print("Starting Wi-Fi SDN Mitigation Simulation")
    print("Dynamic scenarios with 20-30 clients per access point")
    print("Variable APs (1-10) and Attackers (1-10)")
    print("50/50 blocked/unblocked attack distribution")
    
    if args.scenario:
        # Command line mode
        if args.scenario in config.SCENARIOS:
            successful = run_selected_scenario(
                args.scenario, 
                args.runs, 
                not args.no_plots
            )
            print(f"\nScenario {args.scenario} completed")
            print(f"Successful runs: {successful}/{args.runs}")
        else:
            print(f"Error: Scenario '{args.scenario}' not found")
            print("Available scenarios:")
            for scenario_id in config.SCENARIOS.keys():
                print(f"  {scenario_id}")
        return
    
    # Interactive mode
    while True:
        display_scenario_menu()
        choice = get_user_choice()
        
        if choice == 'Q':
            print("\nExiting simulation...")
            break
        elif choice == 'GUI':
            launch_gui()
            break
            
        start_time = time.time()
        
        if choice == 'ALL':
            total_successful = 0
            total_runs = 20 * len(config.SCENARIOS)
            
            for scenario_id in config.SCENARIOS.keys():
                successful = run_selected_scenario(scenario_id)
                total_successful += successful
            
            total_time = time.time() - start_time
            print(f"\nAll scenarios completed in {total_time:.2f} seconds")
            print(f"Total successful runs: {total_successful}/{total_runs}")
        else:
            # Get simulation parameters
            try:
                num_runs = int(input(f"Number of runs (default 20): ") or "20")
                generate_plots = input("Generate plots? (y/n, default y): ").lower() != 'n'
            except ValueError:
                print("Using default values")
                num_runs = 20
                generate_plots = True
            
            successful = run_selected_scenario(choice, num_runs, generate_plots)
            total_time = time.time() - start_time
            print(f"\nScenario {choice} completed in {total_time:.2f} seconds")
            print(f"Successful runs: {successful}/{num_runs}")
        
        # Ask if user wants to run another simulation
        another = input("\nRun another simulation? (Y/N): ").strip().upper()
        if another != 'Y':
            print("\nExiting simulation...")
            break

if __name__ == "__main__":
    main()