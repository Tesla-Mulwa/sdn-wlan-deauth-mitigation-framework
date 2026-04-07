import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import config
from datetime import datetime
import math

class NetworkVisualizer:
    def __init__(self, save_plots=True, show_plots=False):
        self.save_plots = save_plots
        self.show_plots = show_plots
        self.plot_dir = "plots"
        self.ensure_plot_directory()
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette(config.VISUALIZATION_CONFIG["color_palette"])
        
    def ensure_plot_directory(self):
        """Create plots directory if it doesn't exist"""
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)
    
    def load_scenario_data(self, scenario_id):
        """Load CSV data for a specific scenario"""
        try:
            clean_name = scenario_id.replace(' ', '_').replace('/', '_')
            filename = f"data/{clean_name}_results.csv"
            
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                return df
            else:
                print(f"Warning: No data file found for {scenario_id}")
                return None
        except Exception as e:
            print(f"Error loading data for {scenario_id}: {str(e)}")
            return None
    
    def plot_latency_over_runs(self, scenario_id, df):
        """Create line plot showing latency metrics over runs"""
        if df is None or df.empty:
            print(f"No data available for {scenario_id}")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Latency Analysis - {scenario_id}', fontsize=16, fontweight='bold')
        
        # Filter for unblocked runs only
        unblocked_df = df[df['attack_blocked'] == 0]
        
        # Mitigation latency (unblocked runs only)
        if len(unblocked_df) > 0:
            axes[0, 0].plot(unblocked_df['run'], unblocked_df['mitigation_latency_ms'], 'o-', linewidth=2, markersize=6)
        else:
            axes[0, 0].plot(df['run'], df['mitigation_latency_ms'], 'o-', linewidth=2, markersize=6)
        axes[0, 0].set_title('Mitigation Latency Over Runs (Unblocked)')
        axes[0, 0].set_xlabel('Run Number')
        axes[0, 0].set_ylabel('Latency (ms)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Rerouting latency (unblocked runs only)
        if len(unblocked_df) > 0:
            axes[0, 1].plot(unblocked_df['run'], unblocked_df['rerouting_latency_ms'], 's-', linewidth=2, markersize=6, color='orange')
        else:
            axes[0, 1].plot(df['run'], df['rerouting_latency_ms'], 's-', linewidth=2, markersize=6, color='orange')
        axes[0, 1].set_title('Rerouting Latency Over Runs (Unblocked)')
        axes[0, 1].set_xlabel('Run Number')
        axes[0, 1].set_ylabel('Latency (ms)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Restoration latency (unblocked runs only)
        if len(unblocked_df) > 0:
            axes[1, 0].plot(unblocked_df['run'], unblocked_df['restoration_latency_ms'], '^-', linewidth=2, markersize=6, color='green')
        else:
            axes[1, 0].plot(df['run'], df['restoration_latency_ms'], '^-', linewidth=2, markersize=6, color='green')
        axes[1, 0].set_title('Restoration Latency Over Runs (Unblocked)')
        axes[1, 0].set_xlabel('Run Number')
        axes[1, 0].set_ylabel('Latency (ms)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Average latency comparison (only for unblocked runs)
        unblocked_df = df[df['attack_blocked'] == 0]
        if len(unblocked_df) > 0:
            avg_latencies = {
                'Mitigation': unblocked_df['mitigation_latency_ms'].mean(),
                'Rerouting': unblocked_df['rerouting_latency_ms'].mean(),
                'Restoration': unblocked_df['restoration_latency_ms'].mean()
            }
        else:
            avg_latencies = {
                'Mitigation': df['mitigation_latency_ms'].mean(),
                'Rerouting': df['rerouting_latency_ms'].mean(),
                'Restoration': df['restoration_latency_ms'].mean()
            }
        axes[1, 1].bar(avg_latencies.keys(), avg_latencies.values(), color=['blue', 'orange', 'green'])
        axes[1, 1].set_title('Average Latency Comparison (Unblocked Runs)')
        axes[1, 1].set_ylabel('Average Latency (ms)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if self.save_plots:
            filename = f"{self.plot_dir}/{scenario_id.replace(' ', '_').replace('/', '_')}_latency_analysis.png"
            plt.savefig(filename, dpi=config.VISUALIZATION_CONFIG["plot_dpi"], bbox_inches='tight')
            print(f"Latency plot saved: {filename}")
        
        if self.show_plots:
            plt.show()
        else:
            plt.close()
    
    def plot_success_rates(self, scenario_id, df):
        """Create bar charts for success rates"""
        if df is None or df.empty:
            print(f"No data available for {scenario_id}")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Success Rate Analysis - {scenario_id}', fontsize=16, fontweight='bold')
        
        # Filter for unblocked runs only
        unblocked_df = df[df['attack_blocked'] == 0]
        
        # Rerouting success rate over runs (unblocked only)
        if len(unblocked_df) > 0:
            axes[0, 0].plot(unblocked_df['run'], unblocked_df['rerouting_success_rate'], 'o-', linewidth=2, markersize=6, color='blue')
        else:
            axes[0, 0].plot(df['run'], df['rerouting_success_rate'], 'o-', linewidth=2, markersize=6, color='blue')
        axes[0, 0].set_title('Rerouting Success Rate Over Runs (Unblocked)')
        axes[0, 0].set_xlabel('Run Number')
        axes[0, 0].set_ylabel('Success Rate (%)')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim(0, 100)
        
        # Restoration success rate over runs (unblocked only)
        if len(unblocked_df) > 0:
            axes[0, 1].plot(unblocked_df['run'], unblocked_df['restoration_success_rate'], 's-', linewidth=2, markersize=6, color='green')
        else:
            axes[0, 1].plot(df['run'], df['restoration_success_rate'], 's-', linewidth=2, markersize=6, color='green')
        axes[0, 1].set_title('Restoration Success Rate Over Runs (Unblocked)')
        axes[0, 1].set_xlabel('Run Number')
        axes[0, 1].set_ylabel('Success Rate (%)')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_ylim(0, 100)
        
        # Average success rates comparison (only for unblocked runs)
        unblocked_df = df[df['attack_blocked'] == 0]
        avg_success = {
            'Rerouting': unblocked_df['rerouting_success_rate'].mean() if len(unblocked_df) > 0 else 0,
            'Restoration': unblocked_df['restoration_success_rate'].mean() if len(unblocked_df) > 0 else 0
        }
        axes[1, 0].bar(avg_success.keys(), avg_success.values(), color=['blue', 'green'])
        axes[1, 0].set_title('Average Success Rates (Unblocked Runs)')
        axes[1, 0].set_ylabel('Success Rate (%)')
        axes[1, 0].set_ylim(0, 100)
        axes[1, 0].grid(True, alpha=0.3)
        
        # Success rate distribution (only for unblocked runs)
        if len(unblocked_df) > 0:
            axes[1, 1].hist([unblocked_df['rerouting_success_rate'], unblocked_df['restoration_success_rate']], 
                            label=['Rerouting', 'Restoration'], alpha=0.7, bins=10)
        else:
            # No unblocked runs to show
            axes[1, 1].text(0.5, 0.5, 'No unblocked runs', ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Success Rate Distribution (Unblocked Runs)')
            axes[1, 1].set_xlabel('Success Rate (%)')
            axes[1, 1].set_ylabel('Frequency')
            axes[1, 1].grid(True, alpha=0.3)
            return
        axes[1, 1].set_title('Success Rate Distribution (Unblocked Runs)')
        axes[1, 1].set_xlabel('Success Rate (%)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if self.save_plots:
            filename = f"{self.plot_dir}/{scenario_id.replace(' ', '_').replace('/', '_')}_success_rates.png"
            plt.savefig(filename, dpi=config.VISUALIZATION_CONFIG["plot_dpi"], bbox_inches='tight')
            print(f"Success rates plot saved: {filename}")
        
        if self.show_plots:
            plt.show()
        else:
            plt.close()
    
    def plot_throughput_analysis(self, scenario_id, df):
        """Create throughput analysis plots"""
        if df is None or df.empty:
            print(f"No data available for {scenario_id}")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Throughput Analysis - {scenario_id}', fontsize=16, fontweight='bold')
        
        # Throughput over runs
        axes[0, 0].plot(df['run'], df['throughput'], 'o-', linewidth=2, markersize=6, color='purple')
        axes[0, 0].set_title('Throughput Over Runs')
        axes[0, 0].set_xlabel('Run Number')
        axes[0, 0].set_ylabel('Throughput (Mbps)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Throughput percentage over runs
        axes[0, 1].plot(df['run'], df['throughput_percentage'], 's-', linewidth=2, markersize=6, color='red')
        axes[0, 1].set_title('Throughput Percentage Over Runs')
        axes[0, 1].set_xlabel('Run Number')
        axes[0, 1].set_ylabel('Throughput (%)')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_ylim(0, 100)
        
        # Packet loss rate over runs
        axes[1, 0].plot(df['run'], df['packet_loss_rate'], '^-', linewidth=2, markersize=6, color='orange')
        axes[1, 0].set_title('Packet Loss Rate Over Runs')
        axes[1, 0].set_xlabel('Run Number')
        axes[1, 0].set_ylabel('Packet Loss Rate (%)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Throughput vs Packet Loss scatter
        axes[1, 1].scatter(df['packet_loss_rate'], df['throughput'], alpha=0.7, s=50)
        axes[1, 1].set_title('Throughput vs Packet Loss Rate')
        axes[1, 1].set_xlabel('Packet Loss Rate (%)')
        axes[1, 1].set_ylabel('Throughput (Mbps)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if self.save_plots:
            filename = f"{self.plot_dir}/{scenario_id.replace(' ', '_').replace('/', '_')}_throughput_analysis.png"
            plt.savefig(filename, dpi=config.VISUALIZATION_CONFIG["plot_dpi"], bbox_inches='tight')
            print(f"Throughput plot saved: {filename}")
        
        if self.show_plots:
            plt.show()
        else:
            plt.close()
    
    def plot_spatial_layout(self, scenario_id, scenario_config):
        """Create spatial layout visualization"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Network boundary
        circle = plt.Circle((0, 0), config.SPATIAL_CONFIG["network_radius"], 
                           fill=False, color='gray', linestyle='--', linewidth=2)
        ax.add_patch(circle)
        
        # Plot access points
        ap_positions = config.SPATIAL_CONFIG["ap_positions"]
        aps_in_scenario = scenario_config.get("aps", {}).keys() if isinstance(scenario_config.get("aps"), dict) else scenario_config.get("aps", [])
        
        for ap_name in aps_in_scenario:
            if ap_name in ap_positions:
                x, y = ap_positions[ap_name]["x"], ap_positions[ap_name]["y"]
                ax.scatter(x, y, s=200, c='red', marker='^', label=ap_name, zorder=5)
                ax.annotate(ap_name, (x, y), xytext=(5, 5), textcoords='offset points', 
                           fontsize=12, fontweight='bold')
        
        # Plot clients (simplified representation)
        clients = scenario_config.get("clients", {})
        client_positions = {}
        
        for client_name, client_config in clients.items():
            ap_name = client_config["ap"]
            if ap_name in ap_positions:
                # Add some randomness to client positions around their AP
                base_x, base_y = ap_positions[ap_name]["x"], ap_positions[ap_name]["y"]
                offset_x = np.random.normal(0, 5)  # 5m standard deviation
                offset_y = np.random.normal(0, 5)
                client_x = base_x + offset_x
                client_y = base_y + offset_y
                
                # Ensure client is within network boundary
                distance = math.sqrt(client_x**2 + client_y**2)
                if distance > config.SPATIAL_CONFIG["network_radius"]:
                    # Scale back to boundary
                    scale = config.SPATIAL_CONFIG["network_radius"] / distance
                    client_x *= scale
                    client_y *= scale
                
                client_positions[client_name] = (client_x, client_y)
                ax.scatter(client_x, client_y, s=20, c='blue', alpha=0.6, zorder=3)
        
        # Highlight attack target
        attack_target = scenario_config.get("attack_target")
        if attack_target in ap_positions:
            x, y = ap_positions[attack_target]["x"], ap_positions[attack_target]["y"]
            ax.scatter(x, y, s=300, c='red', marker='^', edgecolors='black', linewidth=3, zorder=6)
            ax.annotate(f"{attack_target} (ATTACK TARGET)", (x, y), xytext=(10, 10), 
                       textcoords='offset points', fontsize=14, fontweight='bold', color='red')
        
        ax.set_xlim(-config.SPATIAL_CONFIG["network_radius"]-10, config.SPATIAL_CONFIG["network_radius"]+10)
        ax.set_ylim(-config.SPATIAL_CONFIG["network_radius"]-10, config.SPATIAL_CONFIG["network_radius"]+10)
        ax.set_aspect('equal')
        ax.set_title(f'Spatial Network Layout - {scenario_id}', fontsize=16, fontweight='bold')
        ax.set_xlabel('X Coordinate (meters)')
        ax.set_ylabel('Y Coordinate (meters)')
        ax.grid(True, alpha=0.3)
        
        # Add legend
        ax.scatter([], [], s=200, c='red', marker='^', label='Access Points')
        ax.scatter([], [], s=20, c='blue', alpha=0.6, label='Clients')
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        
        if self.save_plots:
            filename = f"{self.plot_dir}/{scenario_id.replace(' ', '_').replace('/', '_')}_spatial_layout.png"
            plt.savefig(filename, dpi=config.VISUALIZATION_CONFIG["plot_dpi"], bbox_inches='tight')
            print(f"Spatial layout plot saved: {filename}")
        
        if self.show_plots:
            plt.show()
        else:
            plt.close()
    
    def plot_comprehensive_analysis(self, scenario_id, df, scenario_config):
        """Create comprehensive analysis dashboard"""
        if df is None or df.empty:
            print(f"No data available for {scenario_id}")
            return
        
        fig = plt.figure(figsize=(20, 16))
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle(f'Comprehensive Analysis Dashboard - {scenario_id}', fontsize=20, fontweight='bold')
        
        # 1. Attack blocking effectiveness
        ax1 = fig.add_subplot(gs[0, :2])
        blocked_runs = df[df['attack_blocked'] == 1]
        unblocked_runs = df[df['attack_blocked'] == 0]
        
        ax1.bar(['Blocked', 'Unblocked'], [len(blocked_runs), len(unblocked_runs)], 
                color=['green', 'red'], alpha=0.7)
        ax1.set_title('Attack Blocking Effectiveness')
        ax1.set_ylabel('Number of Runs')
        ax1.text(0.5, 0.9, f'Block Rate: {len(blocked_runs)/len(df)*100:.1f}%', 
                transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
        
        # 2. Client impact analysis (averages only for unblocked runs)
        ax2 = fig.add_subplot(gs[0, 2:])
        unblocked_df = df[df['attack_blocked'] == 0]
        metrics = ['num_attacked_clients', 'num_disconnected', 'num_rerouted', 'num_restored']
        if len(unblocked_df) > 0:
            avg_values = [unblocked_df[metric].mean() for metric in metrics]
        else:
            avg_values = [df[metric].mean() for metric in metrics]
        labels = ['Attacked', 'Disconnected', 'Rerouted', 'Restored']
        
        bars = ax2.bar(labels, avg_values, color=['red', 'orange', 'blue', 'green'], alpha=0.7)
        ax2.set_title('Average Client Impact')
        ax2.set_ylabel('Number of Clients')
        
        # Add value labels on bars
        for bar, value in zip(bars, avg_values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    f'{value:.1f}', ha='center', va='bottom')
        
        # Add network info text
        avg_aps = df['num_aps'].mean()
        avg_attackers = df['num_attackers'].mean()
        ax2.text(0.02, 0.98, f'Avg APs: {avg_aps:.1f}\nAvg Attackers: {avg_attackers:.1f}', 
                transform=ax2.transAxes, verticalalignment='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Add network configuration info
        network_info = f"Network Configuration:\n"
        network_info += f"• APs: {avg_aps:.1f} (range: {df['num_aps'].min()}-{df['num_aps'].max()})\n"
        network_info += f"• Attackers: {avg_attackers:.1f} (range: {df['num_attackers'].min()}-{df['num_attackers'].max()})\n"
        network_info += f"• Total Runs: {len(df)}\n"
        network_info += f"• Blocked: {len(blocked_runs)} ({len(blocked_runs)/len(df)*100:.1f}%)"
        
        # Add network info as a separate text box
        fig.text(0.02, 0.02, network_info, fontsize=9, 
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # 3. Latency trends (only unblocked runs)
        ax3 = fig.add_subplot(gs[1, :2])
        if len(unblocked_df) > 0:
            ax3.plot(unblocked_df['run'], unblocked_df['mitigation_latency_ms'], 'o-', label='Mitigation', linewidth=2)
            ax3.plot(unblocked_df['run'], unblocked_df['rerouting_latency_ms'], 's-', label='Rerouting', linewidth=2)
            ax3.plot(unblocked_df['run'], unblocked_df['restoration_latency_ms'], '^-', label='Restoration', linewidth=2)
        else:
            ax3.text(0.5, 0.5, 'No unblocked runs', ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Latency Trends Over Runs (Unblocked Only)')
        ax3.set_xlabel('Run Number')
        ax3.set_ylabel('Latency (ms)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Success rates (only unblocked runs)
        ax4 = fig.add_subplot(gs[1, 2:])
        if len(unblocked_df) > 0:
            ax4.plot(unblocked_df['run'], unblocked_df['rerouting_success_rate'], 'o-', label='Rerouting', linewidth=2)
            ax4.plot(unblocked_df['run'], unblocked_df['restoration_success_rate'], 's-', label='Restoration', linewidth=2)
        else:
            ax4.text(0.5, 0.5, 'No unblocked runs', ha='center', va='center', transform=ax4.transAxes)
        ax4.set_title('Success Rates Over Runs (Unblocked Only)')
        ax4.set_xlabel('Run Number')
        ax4.set_ylabel('Success Rate (%)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim(0, 100)
        
        # 5. Throughput analysis
        ax5 = fig.add_subplot(gs[2, :2])
        ax5.plot(df['run'], df['throughput'], 'o-', color='purple', linewidth=2)
        ax5.set_title('Throughput Over Runs')
        ax5.set_xlabel('Run Number')
        ax5.set_ylabel('Throughput (Mbps)')
        ax5.grid(True, alpha=0.3)
        
        # 6. Packet loss vs throughput (only unblocked runs)
        ax6 = fig.add_subplot(gs[2, 2:])
        if len(unblocked_df) > 0:
            scatter = ax6.scatter(unblocked_df['packet_loss_rate'], unblocked_df['throughput'], 
                                 c='red', alpha=0.7, s=50, label='Unblocked')
        else:
            ax6.text(0.5, 0.5, 'No unblocked runs', ha='center', va='center', transform=ax6.transAxes)
        ax6.set_title('Throughput vs Packet Loss (Unblocked Only)')
        ax6.set_xlabel('Packet Loss Rate (%)')
        ax6.set_ylabel('Throughput (Mbps)')
        ax6.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax6)
        cbar.set_label('Attack Blocked (1=Yes, 0=No)')
        
        # 7. Performance summary
        ax7 = fig.add_subplot(gs[3, :])
        
        # Calculate summary statistics (only for unblocked runs)
        unblocked_df = df[df['attack_blocked'] == 0]
        rerouting_success_avg = unblocked_df['rerouting_success_rate'].mean() if len(unblocked_df) > 0 else 0
        restoration_success_avg = unblocked_df['restoration_success_rate'].mean() if len(unblocked_df) > 0 else 0
        mitigation_latency_avg = unblocked_df['mitigation_latency_ms'].mean() if len(unblocked_df) > 0 else 0
        throughput_avg = unblocked_df['throughput'].mean() if len(unblocked_df) > 0 else df['throughput'].mean()
        packet_loss_avg = unblocked_df['packet_loss_rate'].mean() if len(unblocked_df) > 0 else 0
        
        summary_stats = {
            'Avg Mitigation Latency': f"{mitigation_latency_avg:.2f} ms",
            'Avg Rerouting Success': f"{rerouting_success_avg:.1f}%",
            'Avg Restoration Success': f"{restoration_success_avg:.1f}%",
            'Avg Throughput': f"{throughput_avg:.1f} Mbps",
            'Avg Packet Loss': f"{packet_loss_avg:.1f}%",
            'Block Rate': f"{len(blocked_runs)/len(df)*100:.1f}%",
            'Avg APs': f"{df['num_aps'].mean():.1f}",
            'Avg Attackers': f"{df['num_attackers'].mean():.1f}"
        }
        
        y_pos = np.arange(len(summary_stats))
        ax7.barh(y_pos, [1]*len(summary_stats), color='lightblue', alpha=0.7)
        ax7.set_yticks(y_pos)
        ax7.set_yticklabels(summary_stats.keys())
        ax7.set_title('Performance Summary')
        
        # Add value labels
        for i, (key, value) in enumerate(summary_stats.items()):
            ax7.text(0.5, i, value, ha='center', va='center', fontweight='bold')
        
        ax7.set_xlim(0, 1)
        ax7.set_xticks([])
        
        plt.tight_layout()
        
        if self.save_plots:
            filename = f"{self.plot_dir}/{scenario_id.replace(' ', '_').replace('/', '_')}_comprehensive_analysis.png"
            plt.savefig(filename, dpi=config.VISUALIZATION_CONFIG["plot_dpi"], bbox_inches='tight')
            print(f"Comprehensive analysis plot saved: {filename}")
        
        if self.show_plots:
            plt.show()
        else:
            plt.close()
    
    def generate_all_plots(self, scenario_id):
        """Generate all plots for a given scenario"""
        print(f"\nGenerating plots for {scenario_id}...")
        
        # Load data
        df = self.load_scenario_data(scenario_id)
        scenario_config = config.SCENARIOS.get(scenario_id)
        
        if df is not None and not df.empty:
            # Generate all plot types
            self.plot_latency_over_runs(scenario_id, df)
            self.plot_success_rates(scenario_id, df)
            self.plot_throughput_analysis(scenario_id, df)
            self.plot_comprehensive_analysis(scenario_id, df, scenario_config)
        
        if scenario_config:
            self.plot_spatial_layout(scenario_id, scenario_config)
        
        print(f"All plots generated for {scenario_id}")
    
    def generate_all_scenario_plots(self):
        """Generate plots for all scenarios"""
        for scenario_id in config.SCENARIOS.keys():
            self.generate_all_plots(scenario_id) 