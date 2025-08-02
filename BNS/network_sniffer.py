#!/usr/bin/env python3
"""
Basic Network Sniffer
A comprehensive network packet analyzer with real-time monitoring capabilities.
"""

import socket
import struct
import textwrap
import binascii
import time
import threading
from datetime import datetime
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP
import json
import queue

class NetworkSniffer:
    def __init__(self):
        self.packets = []
        self.packet_queue = queue.Queue()
        self.is_capturing = False
        self.capture_thread = None
        self.packet_count = 0
        self.interface = None
        self.filter = ""
        
    def get_available_interfaces(self):
        """Get list of available network interfaces"""
        try:
            # Try scapy's get_if_list first
            interfaces = get_if_list()
            if interfaces:
                return interfaces
        except Exception as e:
            print(f"Scapy interface detection failed: {e}")
        
        # Fallback methods for different operating systems
        try:
            import platform
            import subprocess
            
            system = platform.system()
            
            if system == "Windows":
                # Windows-specific interface detection
                try:
                    result = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        interfaces = []
                        lines = result.stdout.split('\n')
                        current_interface = None
                        
                        for line in lines:
                            line = line.strip()
                            if 'adapter' in line.lower() and ':' in line:
                                # Extract interface name
                                interface_name = line.split(':')[0].strip()
                                if interface_name and not any(x in interface_name.lower() for x in ['ethernet adapter', 'wireless lan adapter']):
                                    current_interface = interface_name
                                    interfaces.append(current_interface)
                        
                        if interfaces:
                            return interfaces
                except Exception as e:
                    print(f"Windows interface detection failed: {e}")
            
            elif system == "Linux":
                # Linux-specific interface detection
                try:
                    result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        interfaces = []
                        lines = result.stdout.split('\n')
                        for line in lines:
                            if ':' in line and 'state' in line:
                                # Extract interface name (format: 1: lo: <LOOPBACK,UP,LOWER_UP>)
                                parts = line.split(':')
                                if len(parts) >= 2:
                                    interface_name = parts[1].strip()
                                    if interface_name and not interface_name.startswith('lo'):
                                        interfaces.append(interface_name)
                        
                        if interfaces:
                            return interfaces
                except Exception as e:
                    print(f"Linux interface detection failed: {e}")
            
            elif system == "Darwin":  # macOS
                # macOS-specific interface detection
                try:
                    result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        interfaces = []
                        lines = result.stdout.split('\n')
                        for line in lines:
                            if ':' in line and not line.startswith('\t'):
                                # Extract interface name (format: en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST>)
                                interface_name = line.split(':')[0].strip()
                                if interface_name and not interface_name.startswith('lo'):
                                    interfaces.append(interface_name)
                        
                        if interfaces:
                            return interfaces
                except Exception as e:
                    print(f"macOS interface detection failed: {e}")
            
        except Exception as e:
            print(f"Platform-specific interface detection failed: {e}")
        
        # Final fallback - return common interface names
        print("⚠️  Using fallback interface list")
        return ["eth0", "wlan0", "lo", "en0", "en1"]
    
    def get_interface_info(self, interface):
        """Get detailed information about a network interface"""
        try:
            info = {
                'name': interface,
                'mac': get_if_hwaddr(interface),
                'ip': get_if_addr(interface),
                'netmask': get_if_addr(interface)
            }
            return info
        except Exception as e:
            # Fallback for when interface info is not available
            return {
                'name': interface,
                'mac': 'N/A',
                'ip': 'N/A',
                'netmask': 'N/A',
                'error': str(e)
            }
    
    def packet_callback(self, packet):
        """Callback function for each captured packet"""
        if not self.is_capturing:
            return
            
        packet_info = self.analyze_packet(packet)
        self.packets.append(packet_info)
        self.packet_queue.put(packet_info)
        self.packet_count += 1
        
        # Keep only last 1000 packets in memory
        if len(self.packets) > 1000:
            self.packets.pop(0)
    
    def analyze_packet(self, packet):
        """Analyze a single packet and extract relevant information"""
        packet_info = {
            'timestamp': datetime.now().isoformat(),
            'length': len(packet),
            'protocol': 'Unknown',
            'src_ip': 'Unknown',
            'dst_ip': 'Unknown',
            'src_port': None,
            'dst_port': None,
            'flags': None,
            'payload': None,
            'summary': packet.summary()
        }
        
        # Extract IP layer information
        if IP in packet:
            packet_info['src_ip'] = packet[IP].src
            packet_info['dst_ip'] = packet[IP].dst
            packet_info['protocol'] = packet[IP].proto
            
            # TCP analysis
            if TCP in packet:
                packet_info['src_port'] = packet[TCP].sport
                packet_info['dst_port'] = packet[TCP].dport
                packet_info['flags'] = packet[TCP].flags
                packet_info['protocol'] = 'TCP'
                
                # Extract payload (first 100 bytes)
                if packet.haslayer(Raw):
                    payload = packet[Raw].load
                    packet_info['payload'] = binascii.hexlify(payload[:100]).decode()
            
            # UDP analysis
            elif UDP in packet:
                packet_info['src_port'] = packet[UDP].sport
                packet_info['dst_port'] = packet[UDP].dport
                packet_info['protocol'] = 'UDP'
                
                if packet.haslayer(Raw):
                    payload = packet[Raw].load
                    packet_info['payload'] = binascii.hexlify(payload[:100]).decode()
            
            # ICMP analysis
            elif ICMP in packet:
                packet_info['protocol'] = 'ICMP'
                packet_info['icmp_type'] = packet[ICMP].type
                packet_info['icmp_code'] = packet[ICMP].code
        
        # ARP analysis
        elif ARP in packet:
            packet_info['protocol'] = 'ARP'
            packet_info['src_ip'] = packet[ARP].psrc
            packet_info['dst_ip'] = packet[ARP].pdst
            packet_info['src_mac'] = packet[ARP].hwsrc
            packet_info['dst_mac'] = packet[ARP].hwdst
        
        # Ethernet layer
        if Ether in packet:
            packet_info['src_mac'] = packet[Ether].src
            packet_info['dst_mac'] = packet[Ether].dst
        
        return packet_info
    
    def start_capture(self, interface=None, filter_str=""):
        """Start packet capture on specified interface"""
        if self.is_capturing:
            return False
            
        self.interface = interface
        self.filter = filter_str
        self.is_capturing = True
        self.packet_count = 0
        
        def capture_packets():
            try:
                sniff(
                    iface=interface,
                    prn=self.packet_callback,
                    filter=filter_str,
                    store=0,
                    stop_filter=lambda x: not self.is_capturing
                )
            except Exception as e:
                print(f"Capture error: {e}")
        
        self.capture_thread = threading.Thread(target=capture_packets, daemon=True)
        self.capture_thread.start()
        return True
    
    def stop_capture(self):
        """Stop packet capture"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join(timeout=1)
        return True
    
    def get_packet_stats(self):
        """Get statistics about captured packets"""
        if not self.packets:
            return {}
        
        protocols = {}
        ips = {}
        ports = {}
        
        for packet in self.packets:
            # Protocol stats
            protocol = packet.get('protocol', 'Unknown')
            protocols[protocol] = protocols.get(protocol, 0) + 1
            
            # IP stats
            src_ip = packet.get('src_ip', 'Unknown')
            if src_ip != 'Unknown':
                ips[src_ip] = ips.get(src_ip, 0) + 1
            
            # Port stats
            src_port = packet.get('src_port')
            if src_port:
                ports[src_port] = ports.get(src_port, 0) + 1
        
        return {
            'total_packets': len(self.packets),
            'protocols': protocols,
            'top_ips': dict(sorted(ips.items(), key=lambda x: x[1], reverse=True)[:10]),
            'top_ports': dict(sorted(ports.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def get_recent_packets(self, count=50):
        """Get the most recent packets"""
        return self.packets[-count:] if self.packets else []
    
    def clear_packets(self):
        """Clear all stored packets"""
        self.packets.clear()
        self.packet_count = 0
    
    def export_packets(self, filename):
        """Export captured packets to a file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.packets, f, indent=2)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False

# Global sniffer instance
sniffer = NetworkSniffer()

if __name__ == "__main__":
    # Example usage
    print("Network Sniffer - Basic Usage")
    print("Available interfaces:")
    
    sniffer = NetworkSniffer()
    interfaces = sniffer.get_available_interfaces()
    
    if not interfaces:
        print("❌ No network interfaces found!")
        print("\nTroubleshooting:")
        print("1. Make sure you're running as Administrator")
        print("2. Install Npcap from: https://npcap.com/")
        print("3. Or install WinPcap from: https://www.winpcap.org/")
        print("4. Restart your computer after installation")
        print("\nAlternative: Use the web interface which may work without packet capture")
        print("Run: python app.py")
    else:
        for i, interface in enumerate(interfaces):
            print(f"{i+1}. {interface}")
        
        print(f"\nStarting capture on {interfaces[0]}...")
        sniffer.start_capture(interfaces[0])
        
        try:
            while True:
                time.sleep(1)
                stats = sniffer.get_packet_stats()
                print(f"\rCaptured {stats.get('total_packets', 0)} packets", end='')
        except KeyboardInterrupt:
            print("\nStopping capture...")
            sniffer.stop_capture() 