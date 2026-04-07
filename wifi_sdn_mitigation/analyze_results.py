#!/usr/bin/env python3
"""
Analysis script for WiFi SDN Mitigation Simulation Results
Provides comprehensive overview of all scenarios
"""

import pandas as pd
import os
import sys

def analyze_scenario_results(scenario_id, df):
    """Analyze results for a specific scenario"""
    print(f"\n{'='*60}")
    print(f"SCENARIO ANALYSIS: {scenario_id}")
    print(f"{'='*60}")
    
    # Basic statistics
    total_runs = len(df)
    blocked_runs = len(df[df['attack_blocked'] == 1])
    unblocked_runs = len(df[df['attack_blocked'] == 0])
    block_rate = (blocked_runs / total_runs) * 100
    
    print(f"📊 SIMULATION OVERVIEW:")
    print(f"   Total Runs: {total_runs}")
    print(f"   Blocked Runs: {blocked_runs} ({block_rate:.1f}%)")
    print(f"   Unblocked Runs: {unblocked_runs} ({100-block_rate:.1f}%)")
    print(f"   Average Attacked Clients: {df['num_attacked_clients'].mean():.1f}")
    print(f"   Average Number of APs: {df['num_aps'].mean():.1f}")
    print(f"   Average Number of Attackers: {df['num_attackers'].mean():.1f}")
    
    # Performance metrics for unblocked runs (only for the 10 cases where there is no blocking)
    unblocked_df = df[df['attack_blocked'] == 0]
    if len(unblocked_df) > 0:
        print(f"\n🎯 UNBLOCKED ATTACK PERFORMANCE ({len(unblocked_df)} cases):")
        print(f"   Average Disconnected Clients: {unblocked_df['num_disconnected'].mean():.1f}")
        print(f"   Average Rerouted Clients: {unblocked_df['num_rerouted'].mean():.1f}")
        print(f"   Average Restored Clients: {unblocked_df['num_restored'].mean():.1f}")
        print(f"   Average Rerouting Success Rate: {unblocked_df['rerouting_success_rate'].mean():.1f}%")
        print(f"   Average Restoration Success Rate: {unblocked_df['restoration_success_rate'].mean():.1f}%")
        
        print(f"\n⏱️ LATENCY ANALYSIS (Unblocked cases only):")
        print(f"   Average Mitigation Latency: {unblocked_df['mitigation_latency_ms'].mean():.2f} ms")
        print(f"   Average Rerouting Latency: {unblocked_df['rerouting_latency_ms'].mean():.2f} ms")
        print(f"   Average Restoration Latency: {unblocked_df['restoration_latency_ms'].mean():.2f} ms")
        
        print(f"\n📈 NETWORK PERFORMANCE (Unblocked cases only):")
        print(f"   Average Packet Loss Rate: {unblocked_df['packet_loss_rate'].mean():.2f}%")
        print(f"   Average Throughput: {unblocked_df['throughput'].mean():.2f} Mbps")
        print(f"   Average Throughput Percentage: {unblocked_df['throughput_percentage'].mean():.1f}%")
    
    # Performance metrics for blocked runs
    blocked_df = df[df['attack_blocked'] == 1]
    if len(blocked_df) > 0:
        print(f"\n🛡️ BLOCKED ATTACK PERFORMANCE:")
        print(f"   Average Throughput: {blocked_df['throughput'].mean():.2f} Mbps")
        print(f"   Average Throughput Percentage: {blocked_df['throughput_percentage'].mean():.1f}%")
        print(f"   Packet Loss Rate: 0% (perfect protection)")
    
    # Overall performance (unblocked runs only for relevant metrics)
    print(f"\n🏆 OVERALL PERFORMANCE:")
    print(f"   Average Throughput (All Runs): {df['throughput'].mean():.2f} Mbps")
    print(f"   Average Throughput Percentage: {df['throughput_percentage'].mean():.1f}%")
    print(f"   Average Packet Loss Rate (Unblocked): {unblocked_df['packet_loss_rate'].mean():.2f}%" if len(unblocked_df) > 0 else "   Average Packet Loss Rate (Unblocked): 0.00%")
    
    return {
        'total_runs': total_runs,
        'block_rate': block_rate,
        'avg_throughput': df['throughput'].mean(),
        'avg_throughput_percentage': df['throughput_percentage'].mean(),
        'avg_packet_loss': unblocked_df['packet_loss_rate'].mean() if len(unblocked_df) > 0 else 0,
        'avg_rerouting_success': unblocked_df['rerouting_success_rate'].mean() if len(unblocked_df) > 0 else 0,
        'avg_restoration_success': unblocked_df['restoration_success_rate'].mean() if len(unblocked_df) > 0 else 0,
        'avg_aps': df['num_aps'].mean(),
        'avg_attackers': df['num_attackers'].mean()
    }

def compare_scenarios(scenario_stats):
    """Compare performance across all scenarios"""
    print(f"\n{'='*80}")
    print(f"SCENARIO COMPARISON SUMMARY")
    print(f"{'='*80}")
    
    print(f"{'Scenario':<25} {'Block Rate':<12} {'Throughput':<12} {'Packet Loss':<12} {'Reroute Success':<15} {'Restore Success':<15} {'APs':<8} {'Attackers':<10}")
    print(f"{'-'*25} {'-'*12} {'-'*12} {'-'*12} {'-'*15} {'-'*15} {'-'*8} {'-'*10}")
    
    for scenario_id, stats in scenario_stats.items():
        print(f"{scenario_id:<25} {stats['block_rate']:<11.1f}% {stats['avg_throughput']:<11.2f} {stats['avg_packet_loss']:<11.2f}% {stats['avg_rerouting_success']:<14.1f}% {stats['avg_restoration_success']:<14.1f}% {stats['avg_aps']:<7.1f} {stats['avg_attackers']:<9.1f}")
    
    print(f"\n📋 KEY INSIGHTS:")
    
    # Find best performing scenario
    best_throughput = max(stats['avg_throughput'] for stats in scenario_stats.values())
    best_scenario = [k for k, v in scenario_stats.items() if v['avg_throughput'] == best_throughput][0]
    print(f"   🥇 Best Throughput: {best_scenario} ({best_throughput:.2f} Mbps)")
    
    # Find highest block rate
    best_block_rate = max(stats['block_rate'] for stats in scenario_stats.values())
    best_block_scenario = [k for k, v in scenario_stats.items() if v['block_rate'] == best_block_rate][0]
    print(f"   🛡️ Highest Block Rate: {best_block_scenario} ({best_block_rate:.1f}%)")
    
    # Find lowest packet loss
    lowest_packet_loss = min(stats['avg_packet_loss'] for stats in scenario_stats.values())
    best_loss_scenario = [k for k, v in scenario_stats.items() if v['avg_packet_loss'] == lowest_packet_loss][0]
    print(f"   📉 Lowest Packet Loss: {best_loss_scenario} ({lowest_packet_loss:.2f}%)")

def main():
    """Main analysis function"""
    print("WiFi SDN Mitigation Simulation - Results Analysis")
    print("="*80)
    
    # Load all scenario results
    scenario_stats = {}
    
    scenarios = [
        "S1 (3 APs/Dynamic)",
        "S2 (5 APs/Dynamic)", 
        "S3 (7 APs/Dynamic)"
    ]
    
    for scenario_id in scenarios:
        filename = f"data/{scenario_id.replace(' ', '_').replace('/', '_')}_results.csv"
        
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename)
                stats = analyze_scenario_results(scenario_id, df)
                scenario_stats[scenario_id] = stats
            except Exception as e:
                print(f"Error analyzing {scenario_id}: {e}")
        else:
            print(f"⚠️  No data file found for {scenario_id}")
    
    if scenario_stats:
        compare_scenarios(scenario_stats)
        
        print(f"\n🎯 RECOMMENDATIONS:")
        print(f"   • For maximum throughput: Use the scenario with highest throughput")
        print(f"   • For security focus: Use the scenario with highest block rate")
        print(f"   • For reliability: Use the scenario with lowest packet loss")
        print(f"   • For scalability: Consider the scenario with most APs for larger networks")
        
        print(f"\n📊 VISUALIZATION:")
        print(f"   Run 'python main.py --gui' to generate interactive plots")
        print(f"   Or use the visualization module to create detailed charts")
        
    else:
        print("❌ No scenario data found. Please run simulations first.")

if __name__ == "__main__":
    main() 