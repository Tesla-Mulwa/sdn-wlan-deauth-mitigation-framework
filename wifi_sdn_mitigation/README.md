# WiFi SDN Mitigation Simulation

A comprehensive simulation framework for WiFi Software-Defined Network (SDN) attack mitigation strategies. This project simulates various network scenarios with dynamic client allocation, attack detection, and automatic mitigation responses.

## Features

### 🚀 Dynamic Client Allocation
- **10-30 clients per access point** depending on scenario
- **Automatic capacity management** for each AP
- **Random client distribution** with realistic network topologies
- **Spatial layout visualization** with 100-meter radius network

### 📊 Advanced Visualization
- **Line plots** for latency trends over runs
- **Bar charts** for success rates comparison
- **Scatter plots** for throughput vs packet loss analysis
- **Spatial network layouts** with AP and client positions
- **Comprehensive dashboards** with multiple metrics

### 🖥️ Graphical User Interface
- **Intuitive GUI** built with tkinter
- **Real-time progress tracking** with progress bars
- **Live log display** showing simulation events
- **Interactive scenario selection** and parameter configuration
- **One-click plot generation** and visualization

### 🔧 Enhanced Simulation Features
- **Configurable attack blocking** (0-100% blocked runs)
- **Dynamic scenario generation** with random client counts
- **Realistic network behavior** with packet loss and throughput simulation
- **Comprehensive metrics collection** and CSV logging

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd wifi_sdn_mitigation
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python main.py --help
   ```

## Usage

### Command Line Interface

#### Interactive Mode
   ```bash
   python main.py
   ```
This launches an interactive menu where you can:
- Select scenarios to run
- Configure number of runs and blocked percentage
- Choose whether to generate plots
- Launch the GUI

#### Direct Scenario Execution
```bash
python main.py --scenario "S1 (3 APs/Dynamic)" --runs 30 --blocked-percent 60
```

#### GUI Mode
```bash
python main.py --gui
```

### GUI Mode

The GUI provides a comprehensive interface for:
- **Scenario Selection**: Choose from available scenarios
- **Parameter Configuration**: Set runs, blocked percentage
- **Real-time Monitoring**: Watch simulation progress
- **Results Display**: View metrics and statistics
- **Plot Generation**: Create visualizations with one click

### Available Scenarios

1. **S1 (3 APs/Dynamic)**: 3 access points with 30-90 total clients
2. **S2 (5 APs/Dynamic)**: 5 access points with 50-150 total clients  
3. **S3 (7 APs/Dynamic)**: 7 access points with 70-210 total clients

Each scenario dynamically generates:
- Random client counts (10-30 per AP)
- Realistic network topologies
- Appropriate backup AP configurations
- Capacity management based on client load

## Visualization Features

### Generated Plot Types

1. **Latency Analysis**
   - Mitigation latency over runs
   - Rerouting latency trends
   - Restoration latency patterns
   - Average latency comparisons

2. **Success Rate Analysis**
   - Rerouting success rates
   - Restoration success rates
   - Success rate distributions
   - Performance comparisons

3. **Throughput Analysis**
   - Throughput over runs
   - Packet loss rate analysis
   - Throughput vs packet loss correlation
   - Performance degradation patterns

4. **Spatial Network Layout**
   - 100-meter radius network visualization
   - AP positions and coverage areas
   - Client distribution patterns
   - Attack target highlighting

5. **Comprehensive Dashboard**
   - Attack blocking effectiveness
   - Client impact analysis
   - Performance summary statistics
   - Multi-metric correlation analysis

### Plot Configuration

Plots are automatically saved in the `plots/` directory with:
- High-resolution PNG format (300 DPI)
- Professional styling with seaborn
- Consistent color schemes
- Clear titles and labels

## File Structure

```
wifi_sdn_mitigation/
├── main.py              # Main entry point
├── config.py            # Configuration and scenario definitions
├── simulator.py         # Core simulation engine
├── controller.py        # SDN controller logic
├── network.py           # Network components (APs, clients, attackers)
├── metrics.py           # Metrics logging and CSV output
├── visualization.py     # Plot generation and analysis
├── gui.py              # Graphical user interface
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── data/               # CSV results storage
│   ├── S1_(3_APs_Dynamic)_results.csv
│   ├── S2_(5_APs_Dynamic)_results.csv
│   └── S3_(7_APs_Dynamic)_results.csv
└── plots/              # Generated visualizations
    ├── S1_(3_APs_Dynamic)_latency_analysis.png
    ├── S1_(3_APs_Dynamic)_success_rates.png
    ├── S1_(3_APs_Dynamic)_throughput_analysis.png
    ├── S1_(3_APs_Dynamic)_spatial_layout.png
    └── S1_(3_APs_Dynamic)_comprehensive_analysis.png
```

## Configuration

### Scenario Configuration

Scenarios are dynamically generated with:
- **Random client allocation** (10-30 per AP)
- **Automatic capacity management**
- **Realistic backup AP assignments**
- **Spatial positioning** within 100m radius

### Simulation Parameters

- **Detection Probability**: 100% (configurable)
- **Attack Duration**: 5 seconds
- **Ping Interval**: 0.1 seconds
- **Base Throughput**: 25 Mbps
- **Maximum Throughput Deviation**: 7 Mbps

### Visualization Settings

- **Plot Format**: PNG
- **DPI**: 300
- **Figure Size**: 12x8 inches
- **Color Palette**: Professional seaborn colors

## Metrics Collected

### Performance Metrics
- **Attack Blocking Rate**: Percentage of successful blocks
- **Client Impact**: Disconnected, rerouted, restored counts
- **Latency Measurements**: Mitigation, rerouting, restoration times
- **Success Rates**: Rerouting and restoration effectiveness
- **Network Performance**: Throughput and packet loss rates

### Spatial Metrics
- **AP Positions**: X,Y coordinates in 100m radius
- **Client Distribution**: Random positioning around APs
- **Network Coverage**: Visual representation of coverage areas

## Examples

### Running a Quick Test
```bash
python main.py --scenario "S1 (3 APs/Dynamic)" --runs 10 --blocked-percent 50
```

### Generating All Visualizations
```bash
python main.py --scenario "S2 (5 APs/Dynamic)" --runs 20 --blocked-percent 60
```

### Using the GUI
```bash
python main.py --gui
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **GUI Not Launching**: Check tkinter installation
   ```bash
   python -c "import tkinter; print('tkinter available')"
   ```

3. **Plot Generation Fails**: Verify matplotlib and seaborn
   ```bash
   pip install matplotlib seaborn
   ```

4. **Memory Issues**: Reduce number of runs for large scenarios
   ```bash
   python main.py --scenario "S3 (7 APs/Dynamic)" --runs 10
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- SDN architecture concepts
- WiFi network simulation methodologies
- Matplotlib and seaborn visualization libraries
- Tkinter GUI framework