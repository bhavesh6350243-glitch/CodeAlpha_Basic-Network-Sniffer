#!/usr/bin/env python3
"""
Demo Network Sniffer
A demonstration version that generates simulated packet data for testing the interface.
"""

import time
import threading
import random
import json
from datetime import datetime, timedelta
from queue import Queue

class DemoNetworkSniffer:
    def __init__(self):
        self.packets = []
        self.packet_queue = Queue()
        self.is_capturing = False
        self.capture_thread = None
        self.packet_count = 0
        self.interface = "Demo Interface"
        self.filter = ""
        
    def get_available_interfaces(self):
        """Get list of available network interfaces"""
        return ["Demo Interface", "Ethernet", "Wi-Fi", "Loopback"]
    
    def get_interface_info(self, interface):
        """Get detailed information about a network interface"""
        return {
            'name': interface,
            'mac': f"00:1A:2B:3C:4D:{random.randint(10, 99):02d}",
            'ip': f"192.168.1.{random.randint(1, 254)}",
            'netmask': "255.255.255.0"
        }
    
    def generate_demo_packet(self):
        """Generate a simulated packet"""
        protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS']
        protocol = random.choice(protocols)
        
        # Generate random IP addresses
        src_ip = f"192.168.1.{random.randint(1, 254)}"
        dst_ip = f"10.0.0.{random.randint(1, 254)}"
        
        # Generate random ports for TCP/UDP
        src_port = random.randint(1024, 65535) if protocol in ['TCP', 'UDP'] else None
        dst_port = random.randint(1, 1024) if protocol in ['TCP', 'UDP'] else None
        
        packet_info = {
            'timestamp': datetime.now().isoformat(),
            'length': random.randint(64, 1500),
            'protocol': protocol,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'flags': random.choice(['SYN', 'ACK', 'FIN', 'RST']) if protocol == 'TCP' else None,
            'payload': None,
            'summary': f"{protocol} {src_ip}:{src_port or 'N/A'} -> {dst_ip}:{dst_port or 'N/A'}"
        }
        
        return packet_info
    
    def packet_callback(self):
        """Simulate packet callback"""
        if not self.is_capturing:
            return
            
        packet_info = self.generate_demo_packet()
        self.packets.append(packet_info)
        self.packet_queue.put(packet_info)
        self.packet_count += 1
        
        # Keep only last 1000 packets in memory
        if len(self.packets) > 1000:
            self.packets.pop(0)
    
    def start_capture(self, interface=None, filter_str=""):
        """Start simulated packet capture"""
        if self.is_capturing:
            return False
            
        self.interface = interface or "Demo Interface"
        self.filter = filter_str
        self.is_capturing = True
        self.packet_count = 0
        
        def capture_packets():
            try:
                while self.is_capturing:
                    self.packet_callback()
                    # Generate packets at random intervals
                    time.sleep(random.uniform(0.1, 2.0))
            except Exception as e:
                print(f"Demo capture error: {e}")
        
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

# Demo usage
if __name__ == "__main__":
    print("Demo Network Sniffer")
    print("This is a demonstration version that generates simulated packet data.")
    print("Use this for testing the interface without requiring packet capture capabilities.")
    print()
    
    sniffer = DemoNetworkSniffer()
    interfaces = sniffer.get_available_interfaces()
    
    print("Available interfaces:")
    for i, interface in enumerate(interfaces):
        print(f"{i+1}. {interface}")
    
    print(f"\nStarting demo capture on {interfaces[0]}...")
    sniffer.start_capture(interfaces[0])
    
    try:
        while True:
            time.sleep(1)
            stats = sniffer.get_packet_stats()
            print(f"\rDemo: Captured {stats.get('total_packets', 0)} packets", end='')
    except KeyboardInterrupt:
        print("\nStopping demo capture...")
        sniffer.stop_capture() 