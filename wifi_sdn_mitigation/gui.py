import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import sys
import time
from datetime import datetime
import config
from simulator import run_simulation
from visualization import NetworkVisualizer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random

class WiFiSDNGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi SDN Mitigation Simulation")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e3a8a')  # Blue background
        
        # Configure ttk style for blue theme
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base
        style.configure('TLabelframe', background='#e6f3ff', bordercolor='#1e3a8a')
        style.configure('TLabelframe.Label', background='#e6f3ff', foreground='#1e3a8a', font=('Arial', 10, 'bold'))
        style.configure('TButton', background='#1e3a8a', foreground='white')
        style.configure('TLabel', background='#e6f3ff')
        style.configure('TFrame', background='#e6f3ff')
        
        # Initialize components
        self.visualizer = NetworkVisualizer(save_plots=True, show_plots=False)
        self.simulation_running = False
        self.current_scenario = None
        self.simulation_thread = None
        
        # Create GUI components
        self.create_widgets()
        self.update_scenario_info()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="WiFi SDN Mitigation Simulation", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Controls
        left_panel = ttk.LabelFrame(main_frame, text="Simulation Controls", padding="10")
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Scenario selection
        ttk.Label(left_panel, text="Select Scenario:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.scenario_var = tk.StringVar()
        self.scenario_combo = ttk.Combobox(left_panel, textvariable=self.scenario_var, 
                                          state="readonly", width=30)
        self.scenario_combo['values'] = list(config.SCENARIOS.keys())
        self.scenario_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.scenario_combo.bind('<<ComboboxSelected>>', self.on_scenario_change)
        
        # Number of attackers selection
        ttk.Label(left_panel, text="Number of Attackers (1-10):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.attackers_var = tk.IntVar(value=1)
        attackers_spinbox = ttk.Spinbox(left_panel, from_=1, to=10, textvariable=self.attackers_var, width=10)
        attackers_spinbox.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        
        # Number of runs
        ttk.Label(left_panel, text="Number of Runs:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.runs_var = tk.IntVar(value=20)
        runs_spinbox = ttk.Spinbox(left_panel, from_=1, to=100, textvariable=self.runs_var, width=10)
        runs_spinbox.grid(row=5, column=0, sticky=tk.W, pady=(0, 10))
        
        # Attack distribution info
        ttk.Label(left_panel, text="Attack Distribution:").grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Label(left_panel, text="50% Blocked / 50% Unblocked", 
                 font=('Arial', 9, 'italic'), foreground='blue').grid(row=7, column=0, sticky=tk.W, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(left_panel)
        button_frame.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="Start Simulation", 
                                      command=self.start_simulation)
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="Stop Simulation", 
                                     command=self.stop_simulation, state='disabled')
        self.stop_button.grid(row=0, column=1)
        
        # Visualization buttons
        viz_frame = ttk.LabelFrame(left_panel, text="Visualization", padding="5")
        viz_frame.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(viz_frame, text="Generate Plots", 
                  command=self.generate_plots).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(viz_frame, text="Show Plots", 
                  command=self.show_plots).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(viz_frame, text="Open Plot Folder", 
                  command=self.open_plot_folder).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Scenario info
        info_frame = ttk.LabelFrame(left_panel, text="Scenario Information", padding="5")
        info_frame.grid(row=10, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.info_text = tk.Text(info_frame, height=8, width=35, wrap=tk.WORD)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Center panel - Progress and Logs
        center_panel = ttk.LabelFrame(main_frame, text="Simulation Progress", padding="10")
        center_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        center_panel.columnconfigure(0, weight=1)
        center_panel.rowconfigure(1, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(center_panel, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(center_panel, textvariable=self.status_var)
        status_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # Log text
        log_frame = ttk.Frame(center_panel)
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Right panel - Results
        right_panel = ttk.LabelFrame(main_frame, text="Results", padding="10")
        right_panel.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)
        
        # Results tree
        self.results_tree = ttk.Treeview(right_panel, columns=('Value',), show='tree headings')
        self.results_tree.heading('#0', text='Metric')
        self.results_tree.heading('Value', text='Value')
        self.results_tree.column('#0', width=150)
        self.results_tree.column('Value', width=100)
        
        results_scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bottom panel - Quick Stats
        bottom_panel = ttk.LabelFrame(main_frame, text="Quick Statistics", padding="10")
        bottom_panel.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Stats frame
        stats_frame = ttk.Frame(bottom_panel)
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.stats_vars = {}
        stats_labels = ['Total Runs:', 'Successful Runs:', 'Block Rate:', 'Avg Throughput:', 'Avg Latency:']
        
        for i, label in enumerate(stats_labels):
            ttk.Label(stats_frame, text=label).grid(row=i//3, column=(i%3)*2, sticky=tk.W, padx=(0, 5))
            var = tk.StringVar(value="0")
            self.stats_vars[label] = var
            ttk.Label(stats_frame, textvariable=var, font=('Arial', 10, 'bold')).grid(
                row=i//3, column=(i%3)*2+1, sticky=tk.W, padx=(0, 20))
    
    def on_scenario_change(self, event=None):
        """Handle scenario selection change"""
        self.update_scenario_info()
        self.clear_results()
    
    def update_scenario_info(self):
        """Update scenario information display"""
        scenario_id = self.scenario_var.get()
        if not scenario_id:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "Please select a scenario to view information.")
            return
        
        try:
            # Get user-selected number of attackers
            num_attackers = self.attackers_var.get()
            
            # Get default scenario info
            scenario_config = config.SCENARIOS[scenario_id]
            num_clients = len(scenario_config["clients"])
            num_aps = len(scenario_config["aps"])
            
            info_text = f"Scenario: {scenario_id}\n"
            info_text += f"Default APs: {num_aps}\n"
            info_text += f"Default Attackers: {scenario_config.get('num_attackers', 'N/A')}\n"
            info_text += f"Default Clients: {num_clients}\n"
            info_text += f"Attack Target: {scenario_config['attack_target']}\n"
            info_text += f"Expected Attacked: {scenario_config['expected_attacked_clients']}\n\n"
            info_text += f"User Settings:\n"
            info_text += f"Selected Attackers: {num_attackers}\n"
            info_text += f"APs will use default scenario values\n"
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, info_text)
            
        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Error loading scenario info: {str(e)}")
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_simulation(self):
        """Start the simulation in a separate thread"""
        if self.simulation_running:
            return
        
        scenario_id = self.scenario_var.get()
        if not scenario_id:
            messagebox.showerror("Error", "Please select a scenario")
            return
        
        num_runs = self.runs_var.get()
        
        # Generate 50/50 blocked runs distribution
        num_blocked = num_runs // 2
        blocked_runs = set(random.sample(range(1, num_runs + 1), num_blocked))
        
        self.simulation_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.progress_var.set(0)
        self.status_var.set("Starting simulation...")
        
        # Clear previous results
        self.clear_results()
        
        # Start simulation thread
        self.simulation_thread = threading.Thread(
            target=self.run_simulation_thread,
            args=(scenario_id, num_runs, blocked_runs)
        )
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
    
    def run_simulation_thread(self, scenario_id, num_runs, blocked_runs):
        """Run simulation in a separate thread"""
        try:
            # Get user-selected number of attackers only
            num_attackers = self.attackers_var.get()
            
            # Use default scenario but override the number of attackers
            default_scenario = config.SCENARIOS[scenario_id].copy()
            default_scenario["num_attackers"] = num_attackers
            
            successful_runs = 0
            metrics_list = []
            
            for run_id in range(1, num_runs + 1):
                if self.simulation_running:
                    try:
                        # Use modified default scenario
                        metrics = run_simulation(scenario_id, run_id, blocked_runs, default_scenario)
                        if metrics:
                            successful_runs += 1
                            metrics_list.append(metrics)
                            self.log_message(f"Run {run_id}/{num_runs} completed successfully")
                        else:
                            self.log_message(f"Run {run_id} failed")
                    except Exception as e:
                        self.log_message(f"Run {run_id} error: {str(e)}")
                else:
                    break
            
            # Update GUI on main thread
            self.root.after(0, self.simulation_completed, successful_runs, num_runs, metrics_list)
            
        except Exception as e:
            self.log_message(f"Simulation error: {str(e)}")
            self.root.after(0, self.simulation_completed, 0, num_runs, [])
    
    def simulation_completed(self, successful_runs=0, total_runs=0, metrics_list=[]):
        """Handle simulation completion"""
        self.simulation_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress_var.set(100)
        self.status_var.set("Simulation completed")
        
        if successful_runs > 0:
            self.log_message(f"Simulation completed: {successful_runs}/{total_runs} successful runs")
        else:
            self.log_message("Simulation completed with errors")
        
        # Update results
        if metrics_list:
            self.root.after(0, lambda: self.update_results(metrics_list))
    
    def stop_simulation(self):
        """Stop the running simulation"""
        self.simulation_running = False
        self.status_var.set("Stopping simulation...")
        self.log_message("Simulation stopped by user")
    
    def update_results(self, metrics_list):
        """Update results display"""
        if not metrics_list:
            return
        
        # Calculate averages
        df = pd.DataFrame(metrics_list)
        avg_metrics = df.mean()
        
        # Calculate averages for unblocked runs only (for success rates and latencies)
        unblocked_df = df[df['attack_blocked'] == 0]
        if len(unblocked_df) > 0:
            unblocked_avg = unblocked_df.mean()
        else:
            unblocked_avg = avg_metrics
        
        # Clear previous results
        self.results_tree.delete(*self.results_tree.get_children())
        
        # Add results to tree
        results_data = [
            ('Attacked Clients', f"{avg_metrics.get('num_attacked_clients', 0):.1f}"),
            ('Disconnected Clients', f"{avg_metrics.get('num_disconnected', 0):.1f}"),
            ('Rerouted Clients', f"{avg_metrics.get('num_rerouted', 0):.1f}"),
            ('Restored Clients', f"{avg_metrics.get('num_restored', 0):.1f}"),
            ('Mitigation Latency', f"{unblocked_avg.get('mitigation_latency_ms', 0):.2f} ms"),
            ('Rerouting Latency', f"{unblocked_avg.get('rerouting_latency_ms', 0):.2f} ms"),
            ('Restoration Latency', f"{unblocked_avg.get('restoration_latency_ms', 0):.2f} ms"),
            ('Rerouting Success Rate', f"{unblocked_avg.get('rerouting_success_rate', 0):.1f}%"),
            ('Restoration Success Rate', f"{unblocked_avg.get('restoration_success_rate', 0):.1f}%"),
            ('Packet Loss Rate', f"{avg_metrics.get('packet_loss_rate', 0):.1f}%"),
            ('Throughput', f"{avg_metrics.get('throughput', 0):.1f} Mbps"),
            ('Throughput Percentage', f"{avg_metrics.get('throughput_percentage', 0):.1f}%")
        ]
        
        for metric, value in results_data:
            self.results_tree.insert('', 'end', text=metric, values=(value,))
        
        # Update quick stats
        self.stats_vars['Total Runs:'].set(str(len(metrics_list)))
        self.stats_vars['Successful Runs:'].set(str(len(metrics_list)))
        self.stats_vars['Block Rate:'].set(f"{avg_metrics.get('attack_blocked', 0)*100:.1f}%")
        self.stats_vars['Avg Throughput:'].set(f"{avg_metrics.get('throughput', 0):.1f} Mbps")
        self.stats_vars['Avg Latency:'].set(f"{unblocked_avg.get('mitigation_latency_ms', 0):.1f} ms")
    
    def clear_results(self):
        """Clear results display"""
        self.results_tree.delete(*self.results_tree.get_children())
        for var in self.stats_vars.values():
            var.set("0")
    
    def generate_plots(self):
        """Generate plots for current scenario"""
        scenario_id = self.scenario_var.get()
        if not scenario_id:
            messagebox.showerror("Error", "Please select a scenario")
            return
        
        try:
            self.log_message(f"Generating plots for {scenario_id}...")
            self.visualizer.generate_all_plots(scenario_id)
            self.log_message("Plots generated successfully")
            messagebox.showinfo("Success", "Plots generated successfully!")
        except Exception as e:
            self.log_message(f"Error generating plots: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate plots: {str(e)}")
    
    def show_plots(self):
        """Show plots for current scenario"""
        scenario_id = self.scenario_var.get()
        if not scenario_id:
            messagebox.showerror("Error", "Please select a scenario")
            return
        
        try:
            self.log_message(f"Showing plots for {scenario_id}...")
            # Temporarily enable plot display
            self.visualizer.show_plots = True
            self.visualizer.generate_all_plots(scenario_id)
            self.visualizer.show_plots = False
            self.log_message("Plots displayed")
        except Exception as e:
            self.log_message(f"Error showing plots: {str(e)}")
            messagebox.showerror("Error", f"Failed to show plots: {str(e)}")
    
    def open_plot_folder(self):
        """Open the plots folder"""
        try:
            plot_dir = os.path.abspath(self.visualizer.plot_dir)
            if os.path.exists(plot_dir):
                os.startfile(plot_dir)  # Windows
            else:
                messagebox.showinfo("Info", "Plot folder is empty or doesn't exist")
        except Exception as e:
            self.log_message(f"Error opening plot folder: {str(e)}")
            messagebox.showerror("Error", f"Failed to open plot folder: {str(e)}")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = WiFiSDNGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 