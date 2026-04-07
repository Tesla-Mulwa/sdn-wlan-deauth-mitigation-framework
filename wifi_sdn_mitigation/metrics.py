import csv
import os
import config

def log_metrics(metrics, scenario_id):
    try:
        os.makedirs("data", exist_ok=True)
        clean_name = scenario_id.replace(' ', '_').replace('/', '_')
        filename = f"data/{clean_name}_results.csv"
        
        headers = [
            "run", "attack_blocked", "num_attacked_clients",
            "num_disconnected", "num_rerouted", "num_restored",
            "mitigation_latency_ms", "rerouting_latency_ms", "restoration_latency_ms",
            "rerouting_success_rate", "restoration_success_rate",
            "packet_loss_rate", "throughput", "throughput_percentage",
            "num_attackers", "num_aps"
        ]
        
        # Ensure metrics are properly formatted
        metrics["packet_loss_rate"] = round(metrics["packet_loss_rate"], 2)
        metrics["throughput"] = round(metrics["throughput"], 2)
        metrics["throughput_percentage"] = round(metrics["throughput_percentage"], 2)
        
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow(metrics)
        print(f"Metrics saved to {filename}")
        
    except Exception as e:
        print(f"Error saving metrics: {str(e)}")
        try:
            docs_path = os.path.join(os.path.expanduser('~'), 'Documents')
            alt_path = os.path.join(docs_path, 'wifi_sdn_results')
            os.makedirs(alt_path, exist_ok=True)
            alt_file = os.path.join(alt_path, f"{clean_name}_results.csv")
            
            file_exists = os.path.isfile(alt_file)
            with open(alt_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(metrics)
            print(f"Metrics saved to alternative location: {alt_file}")
        except Exception as e2:
            print(f"Failed to save metrics to alternative location: {str(e2)}")