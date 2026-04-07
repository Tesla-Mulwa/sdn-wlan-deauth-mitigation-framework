#!/usr/bin/env python3
"""
Test script to verify latency calculations are working correctly
"""

import pandas as pd
import os
import sys

def test_latency_calculations():
    """Test that latencies are positive and averages are calculated correctly"""
    
    # Check if any data files exist
    data_dir = "data"
    if not os.path.exists(data_dir):
        print("No data directory found. Please run simulations first.")
        return
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('_results.csv')]
    
    if not csv_files:
        print("No CSV files found in data directory. Please run simulations first.")
        return
    
    print("Testing latency calculations...")
    print("="*50)
    
    for csv_file in csv_files:
        filepath = os.path.join(data_dir, csv_file)
        df = pd.read_csv(filepath)
        
        print(f"\nFile: {csv_file}")
        print(f"Total runs: {len(df)}")
        
        # Check for negative latencies
        negative_latencies = df[df['mitigation_latency_ms'] < 0]
        if len(negative_latencies) > 0:
            print(f"❌ Found {len(negative_latencies)} runs with negative mitigation latencies!")
            print(negative_latencies[['run', 'mitigation_latency_ms']].head())
        else:
            print("✅ No negative mitigation latencies found")
        
        # Check rerouting latencies
        negative_rerouting = df[df['rerouting_latency_ms'] < 0]
        if len(negative_rerouting) > 0:
            print(f"❌ Found {len(negative_rerouting)} runs with negative rerouting latencies!")
        else:
            print("✅ No negative rerouting latencies found")
        
        # Check restoration latencies
        negative_restoration = df[df['restoration_latency_ms'] < 0]
        if len(negative_restoration) > 0:
            print(f"❌ Found {len(negative_restoration)} runs with negative restoration latencies!")
        else:
            print("✅ No negative restoration latencies found")
        
        # Check averages for unblocked runs
        unblocked_df = df[df['attack_blocked'] == 0]
        blocked_df = df[df['attack_blocked'] == 1]
        
        print(f"Blocked runs: {len(blocked_df)}")
        print(f"Unblocked runs: {len(unblocked_df)}")
        
        if len(unblocked_df) > 0:
            print(f"Average mitigation latency (unblocked): {unblocked_df['mitigation_latency_ms'].mean():.2f} ms")
            print(f"Average rerouting success rate (unblocked): {unblocked_df['rerouting_success_rate'].mean():.1f}%")
            print(f"Average restoration success rate (unblocked): {unblocked_df['restoration_success_rate'].mean():.1f}%")
        else:
            print("No unblocked runs found")
        
        # Overall averages
        print(f"Overall average mitigation latency: {df['mitigation_latency_ms'].mean():.2f} ms")
        print(f"Overall average rerouting success rate: {df['rerouting_success_rate'].mean():.1f}%")
        print(f"Overall average restoration success rate: {df['restoration_success_rate'].mean():.1f}%")

if __name__ == "__main__":
    test_latency_calculations() 