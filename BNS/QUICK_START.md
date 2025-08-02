# 🚀 Quick Start Guide - Network Sniffer

## ⚡ Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Health Check (Optional but Recommended)
```bash
python start.py --health-check
```

### Step 3: Launch the Application
```bash
python start.py
```

Then choose from the menu:
- **Option 1**: Web Interface (Real packet capture)
- **Option 2**: Demo Mode (Simulated data - No admin privileges needed)
- **Option 3**: Command Line Interface
- **Option 4**: List Network Interfaces
- **Option 5**: Health Check & Diagnostics
- **Option 6**: Exit

## 🎯 Recommended for First-Time Users

### **Demo Mode (Easiest)**
```bash
python start.py --demo
```
Then open: http://localhost:5001

**Why Demo Mode?**
- ✅ No administrator privileges required
- ✅ Works immediately on any system
- ✅ Simulated packet data for testing
- ✅ All features work normally
- ✅ Perfect for learning and testing

### **Web Interface (Real Capture)**
```bash
python start.py --web
```
Then open: http://localhost:5000

**Requirements:**
- Administrator/root privileges
- Npcap or WinPcap installed (Windows)
- Network interface with packet capture capabilities

## 🔧 Troubleshooting

### **Permission Issues**
**Problem**: "Permission denied" or "No interfaces found"
**Solution**: 
- Use Demo Mode: `python start.py --demo`
- Or run as Administrator (Windows) / root (Linux/macOS)

### **Port Already in Use**
**Problem**: "Address already in use"
**Solution**:
- Demo uses port 5001, Web uses port 5000
- Close other applications using these ports
- Or change ports in `config.py`

### **Missing Dependencies**
**Problem**: Import errors
**Solution**:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### **Windows Issues**
**Problem**: No packet capture on Windows
**Solution**:
1. Install Npcap: https://npcap.com/
2. Restart computer
3. Run Command Prompt as Administrator
4. Or use Demo Mode

## 📋 Common Commands

### **Health Check**
```bash
python start.py --health-check
```

### **Demo Mode**
```bash
python start.py --demo
```

### **Web Interface**
```bash
python start.py --web
```

### **CLI Interface**
```bash
python cli_sniffer.py --list
python cli_sniffer.py -i eth0
```

### **Direct Python Usage**
```python
from network_sniffer import NetworkSniffer
sniffer = NetworkSniffer()
interfaces = sniffer.get_available_interfaces()
print("Available interfaces:", interfaces)
```

## 🎯 What You'll See

### **Web Interface Features:**
- Real-time packet monitoring
- Interactive statistics dashboard
- Protocol distribution charts
- Packet details table
- Export functionality
- BPF filter support

### **Demo Mode Features:**
- Simulated packet data
- Same interface as real capture
- No setup required
- Perfect for learning

### **CLI Features:**
- Rich terminal UI
- Live statistics
- Color-coded output
- Export options

## 🔍 Next Steps

1. **Try Demo Mode** to see the interface
2. **Run Health Check** to diagnose issues
3. **Install Npcap** (Windows) for real capture
4. **Explore BPF Filters** for targeted capture
5. **Check the README** for advanced features

## 💡 Tips

- **Demo Mode** is perfect for learning and testing
- **Health Check** helps diagnose setup issues
- **BPF Filters** let you capture specific traffic
- **Export** saves captured data for analysis
- **Web Interface** provides the best user experience

## 🆘 Need Help?

1. Run health check: `python start.py --health-check`
2. Try demo mode: `python start.py --demo`
3. Check the README.md for detailed documentation
4. Look at PROBLEMS_SOLVED.md for common issues

---

**Happy Network Monitoring! 🌐** 