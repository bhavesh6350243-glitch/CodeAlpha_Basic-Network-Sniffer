# Network Sniffer - Real-time Packet Analyzer

A comprehensive network packet analyzer with both web-based and command-line interfaces for real-time network monitoring and analysis.

## 🌟 Features

- **Real-time Packet Capture**: Monitor network traffic in real-time
- **Multiple Interfaces**: Web UI and CLI versions
- **Protocol Analysis**: Support for TCP, UDP, ICMP, ARP, and more
- **BPF Filtering**: Berkeley Packet Filter support for targeted capture
- **Statistics & Analytics**: Live statistics and packet analysis
- **Data Export**: Export captured packets to JSON format
- **Modern UI**: Beautiful, responsive web interface
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Health Check System**: Built-in diagnostics and troubleshooting
- **Demo Mode**: Simulated packet data for testing without privileges
- **Configuration Management**: Centralized settings and environment support

## 📋 Requirements

- Python 3.7 or higher
- Administrator/root privileges (for packet capture)
- Network interface with packet capture capabilities

## 🚀 Quick Start

### **3-Step Setup**

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Health Check** (Recommended):
   ```bash
   python start.py --health-check
   ```

3. **Launch Application**:
   ```bash
   python start.py
   ```

### **For First-Time Users**

**Demo Mode** (Recommended - No admin privileges needed):
```bash
python start.py --demo
```
Then open: http://localhost:5001

**Web Interface** (Real packet capture):
```bash
python start.py --web
```
Then open: http://localhost:5000

## 🎯 Usage

### Demo Mode (Recommended for Testing)

For users who don't have packet capture capabilities or want to test the interface:

```bash
python start.py --demo
```

Or use the interactive menu:
```bash
python start.py
# Then choose option 2: Demo Mode
```

Then open your browser and navigate to:
```
http://localhost:5001
```

**Features:**
- Simulated packet data for testing
- No administrator privileges required
- All interface features work normally
- Perfect for learning and testing

### Web Interface (Real Packet Capture)

Start the web application:
```bash
python start.py --web
```

Then open your browser and navigate to:
```
http://localhost:5000
```

**Features:**
- Real-time packet monitoring
- Interactive statistics dashboard
- Protocol distribution charts
- Packet details table
- Export functionality
- BPF filter support

### Command Line Interface

#### List available interfaces:
```bash
python cli_sniffer.py --list
```

#### Basic capture:
```bash
python cli_sniffer.py --interface eth0
```

#### Capture with filter:
```bash
python cli_sniffer.py -i eth0 -f "tcp port 80"
```

#### Capture specific host:
```bash
python cli_sniffer.py -i eth0 -f "host 192.168.1.1"
```

#### Capture UDP traffic:
```bash
python cli_sniffer.py -i eth0 -f "udp"
```

### Health Check & Diagnostics

Run comprehensive system diagnostics:
```bash
python start.py --health-check
```

**Checks:**
- Python version compatibility
- Dependencies installation
- Administrator privileges
- Network interface availability
- Port availability
- System resources
- File permissions

### Direct Python Usage

```python
from network_sniffer import NetworkSniffer

# Create sniffer instance
sniffer = NetworkSniffer()

# List available interfaces
interfaces = sniffer.get_available_interfaces()
print("Available interfaces:", interfaces)

# Start capture
sniffer.start_capture("eth0", "tcp port 80")

# Get statistics
stats = sniffer.get_packet_stats()
print("Statistics:", stats)

# Stop capture
sniffer.stop_capture()
```

## 🔧 BPF Filter Examples

Berkeley Packet Filter (BPF) allows you to capture specific types of traffic:

| Filter | Description |
|--------|-------------|
| `tcp port 80` | HTTP traffic |
| `tcp port 443` | HTTPS traffic |
| `udp port 53` | DNS queries |
| `host 192.168.1.1` | Traffic to/from specific IP |
| `src host 192.168.1.1` | Traffic from specific IP |
| `dst host 192.168.1.1` | Traffic to specific IP |
| `icmp` | ICMP packets (ping, etc.) |
| `arp` | ARP requests/replies |
| `port 22` | SSH traffic |
| `port 3389` | RDP traffic |

## 📊 Supported Protocols

- **TCP**: Transmission Control Protocol
- **UDP**: User Datagram Protocol
- **ICMP**: Internet Control Message Protocol
- **ARP**: Address Resolution Protocol
- **HTTP/HTTPS**: Web traffic (when using port filters)
- **DNS**: Domain Name System
- **DHCP**: Dynamic Host Configuration Protocol
- **And more...**

## 🛠️ Project Structure

```
cyber security2/
├── app.py                 # Flask web application
├── demo_app.py            # Demo web application
├── network_sniffer.py     # Core sniffer functionality
├── demo_sniffer.py        # Demo sniffer with simulated data
├── cli_sniffer.py         # Command-line interface
├── start.py               # Interactive startup script
├── config.py              # Configuration management
├── logger.py              # Logging system
├── health_check.py        # Health check and diagnostics
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface template
├── README.md             # This file
├── QUICK_START.md        # Quick start guide
└── PROBLEMS_SOLVED.md    # Issues and solutions
```

## 🔍 Features in Detail

### Web Interface
- **Real-time Updates**: Live packet capture with WebSocket updates
- **Interactive Dashboard**: Statistics, charts, and packet tables
- **Responsive Design**: Works on desktop and mobile devices
- **Export Functionality**: Download captured data as JSON
- **Filter Support**: BPF filter input for targeted capture

### Command Line Interface
- **Rich Terminal UI**: Color-coded output with tables
- **Live Updates**: Real-time statistics and packet display
- **Export Options**: Save captured data to files
- **Interface Discovery**: List and validate network interfaces

### Health Check System
- **Comprehensive Diagnostics**: System compatibility checks
- **Dependency Verification**: Ensures all required packages are installed
- **Permission Validation**: Checks administrator/root privileges
- **Resource Monitoring**: Memory, disk space, and port availability
- **Network Interface Detection**: Validates packet capture capabilities

### Core Functionality
- **Packet Analysis**: Deep packet inspection and parsing
- **Protocol Detection**: Automatic protocol identification
- **Statistics Generation**: Real-time analytics and metrics
- **Memory Management**: Efficient packet storage and cleanup
- **Thread Safety**: Multi-threaded capture with proper synchronization

## ⚠️ Important Notes

### Security Considerations
- **Administrator Access**: Packet capture requires elevated privileges
- **Network Monitoring**: Be aware of privacy implications
- **Legal Compliance**: Ensure you have permission to monitor network traffic
- **Data Protection**: Captured data may contain sensitive information

### Performance Considerations
- **Memory Usage**: Large packet captures consume significant memory
- **CPU Usage**: Real-time analysis can be CPU intensive
- **Network Impact**: Capture filters can reduce processing load
- **Storage**: Export large captures may require significant disk space

## 🐛 Troubleshooting

### Common Issues

1. **Permission Denied**
   - **Solution**: Run as administrator/root
   - **Windows**: Right-click Command Prompt → "Run as administrator"
   - **Linux/macOS**: Use `sudo python app.py`
   - **Alternative**: Use Demo Mode which doesn't require privileges

2. **No Interfaces Found**
   - **Solution**: Check if you have network interfaces available
   - **Windows**: Install Npcap from https://npcap.com/ or WinPcap from https://www.winpcap.org/
   - **Linux**: Ensure `libpcap` is installed
   - **Alternative**: Use Demo Mode for testing

3. **Capture Not Starting**
   - **Solution**: Verify interface name and permissions
   - **Check**: Use `--list` to see available interfaces
   - **Test**: Try with a simple filter first
   - **Windows**: Ensure Npcap/WinPcap is installed and restart computer

4. **Web Interface Not Loading**
   - **Solution**: Check if port 5000 is available
   - **Alternative**: Change port in `config.py`
   - **Firewall**: Ensure firewall allows the connection
   - **Demo Mode**: Use `python start.py --demo` for port 5001

5. **Dependencies Installation Issues**
   - **Windows**: If `netifaces` fails to install, the updated requirements.txt should work
   - **Alternative**: Use Demo Mode which has fewer dependencies

6. **Health Check Failures**
   - **Run**: `python start.py --health-check`
   - **Follow**: The diagnostic recommendations
   - **Use**: Demo Mode if real capture fails

### Debug Mode

Enable debug output by modifying the Flask app:
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

## 📈 Advanced Usage

### Custom Filters
```bash
# Capture only HTTP POST requests
python cli_sniffer.py -i eth0 -f "tcp port 80 and tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x504F5354"

# Capture traffic between specific hosts
python cli_sniffer.py -i eth0 -f "host 192.168.1.1 and host 192.168.1.2"

# Capture large packets
python cli_sniffer.py -i eth0 -f "greater 1500"
```

### Integration with Other Tools
```python
# Export to Wireshark format
from scapy.all import wrpcap
packets = sniffer.get_recent_packets()
wrpcap("capture.pcap", packets)

# Analyze with pandas
import pandas as pd
packets = sniffer.get_recent_packets()
df = pd.DataFrame(packets)
print(df.groupby('protocol').size())
```

### Environment Configuration
```bash
# Set custom ports
export WEB_PORT=8080
export DEMO_PORT=8081

# Enable debug mode
export DEBUG_MODE=true

# Set memory limit
export MAX_PACKETS_IN_MEMORY=2000

# Run with custom settings
python start.py --web
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational and legitimate network monitoring purposes only. Users are responsible for complying with applicable laws and regulations.

## ⚖️ Disclaimer

This tool is intended for educational purposes and legitimate network monitoring. Users must:
- Only monitor networks they own or have explicit permission to monitor
- Comply with all applicable laws and regulations
- Respect privacy and data protection requirements
- Use responsibly and ethically

The authors are not responsible for any misuse of this software.

## 🔗 Related Tools

- **Wireshark**: Professional network protocol analyzer
- **tcpdump**: Command-line packet analyzer
- **tshark**: Terminal-based Wireshark
- **nmap**: Network discovery and security auditing

---

**Happy Network Monitoring! 🌐** 