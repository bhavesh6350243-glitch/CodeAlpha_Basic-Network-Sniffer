#!/usr/bin/env python3
"""
Command Line Network Sniffer
A simple terminal-based network packet analyzer.
"""

import argparse
import sys
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress
from network_sniffer import NetworkSniffer

console = Console()

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    NETWORK SNIFFER CLI                       ║
    ║                Real-time Packet Analyzer                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold blue")

def list_interfaces(sniffer):
    """List available network interfaces"""
    console.print("\n[bold]Available Network Interfaces:[/bold]")
    
    try:
        interfaces = sniffer.get_available_interfaces()
    except Exception as e:
        console.print(f"[red]Error getting interfaces: {e}[/red]")
        return False
    
    if not interfaces:
        console.print("[red]No network interfaces found![/red]")
        console.print("\n[yellow]Troubleshooting:[/yellow]")
        console.print("1. Make sure you're running as Administrator")
        console.print("2. Install Npcap from: https://npcap.com/")
        console.print("3. Or install WinPcap from: https://www.winpcap.org/")
        console.print("4. Restart your computer after installation")
        console.print("\n[green]Alternative:[/green] Use the web interface which may work without packet capture")
        console.print("Run: python app.py")
        return False
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Interface", style="cyan")
    table.add_column("IP Address", style="green")
    table.add_column("MAC Address", style="yellow")
    table.add_column("Status", style="blue")
    
    for interface in interfaces:
        try:
            info = sniffer.get_interface_info(interface)
            ip = info.get('ip', 'N/A')
            mac = info.get('mac', 'N/A')
            status = "Available" if ip != 'N/A' else "No IP"
            table.add_row(interface, ip, mac, status)
        except Exception as e:
            table.add_row(interface, "Error", "Error", f"Error: {str(e)[:20]}")
    
    console.print(table)
    return True

def create_stats_table(stats):
    """Create a rich table for statistics"""
    table = Table(title="Packet Statistics", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    if stats:
        table.add_row("Total Packets", str(stats.get('total_packets', 0)))
        table.add_row("Protocols Detected", str(len(stats.get('protocols', {}))))
        table.add_row("Unique IPs", str(len(stats.get('top_ips', {}))))
        table.add_row("Active Ports", str(len(stats.get('top_ports', {}))))
    else:
        table.add_row("Total Packets", "0")
        table.add_row("Protocols Detected", "0")
        table.add_row("Unique IPs", "0")
        table.add_row("Active Ports", "0")
    
    return table

def create_packet_table(packets):
    """Create a rich table for recent packets"""
    table = Table(title="Recent Packets", show_header=True, header_style="bold magenta")
    table.add_column("Time", style="cyan", width=12)
    table.add_column("Protocol", style="green", width=8)
    table.add_column("Source", style="yellow", width=20)
    table.add_column("Destination", style="yellow", width=20)
    table.add_column("Length", style="blue", width=10)
    
    for packet in packets[-10:]:  # Show last 10 packets
        time_str = datetime.fromisoformat(packet['timestamp']).strftime('%H:%M:%S')
        protocol = packet.get('protocol', 'Unknown')
        src = packet.get('src_ip', packet.get('src_mac', 'Unknown'))
        dst = packet.get('dst_ip', packet.get('dst_mac', 'Unknown'))
        length = packet.get('length', 0)
        
        # Color code protocols
        protocol_style = {
            'TCP': 'bold blue',
            'UDP': 'bold red',
            'ICMP': 'bold yellow',
            'ARP': 'bold magenta'
        }.get(protocol, 'bold white')
        
        table.add_row(
            time_str,
            Text(protocol, style=protocol_style),
            src[:18] + '...' if len(src) > 18 else src,
            dst[:18] + '...' if len(dst) > 18 else dst,
            f"{length} bytes"
        )
    
    return table

def live_capture(interface, filter_str="", max_packets=1000):
    """Live packet capture with real-time display"""
    sniffer = NetworkSniffer()
    
    console.print(f"\n[bold green]Starting capture on interface:[/bold green] {interface}")
    if filter_str:
        console.print(f"[bold yellow]Filter:[/bold yellow] {filter_str}")
    
    # Start capture
    if not sniffer.start_capture(interface, filter_str):
        console.print("[red]Failed to start capture![/red]")
        return
    
    console.print("\n[bold]Press Ctrl+C to stop capture[/bold]\n")
    
    try:
        with Live(auto_refresh=True, refresh_per_second=4) as live:
            while True:
                # Get current stats and packets
                stats = sniffer.get_packet_stats()
                packets = sniffer.get_recent_packets(10)
                
                # Create layout
                stats_table = create_stats_table(stats)
                packet_table = create_packet_table(packets)
                
                # Combine tables
                layout = f"{stats_table}\n\n{packet_table}"
                
                # Add status panel
                status = f"Capturing: {'[green]ACTIVE[/green]' if sniffer.is_capturing else '[red]STOPPED[/red]'}"
                status += f" | Packets: {sniffer.packet_count}"
                status += f" | Interface: {interface}"
                
                panel = Panel(layout, title=status, border_style="blue")
                live.update(panel)
                
                time.sleep(0.25)  # Update 4 times per second
                
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Stopping capture...[/bold yellow]")
        sniffer.stop_capture()
        
        # Final statistics
        final_stats = sniffer.get_packet_stats()
        console.print("\n[bold]Final Statistics:[/bold]")
        console.print(create_stats_table(final_stats))
        
        # Export option
        if final_stats.get('total_packets', 0) > 0:
            export = console.input("\n[bold]Export packets to file? (y/n): [/bold]")
            if export.lower() == 'y':
                filename = f"packets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                if sniffer.export_packets(filename):
                    console.print(f"[green]Packets exported to: {filename}[/green]")
                else:
                    console.print("[red]Export failed![/red]")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Network Sniffer CLI - Real-time packet analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_sniffer.py --list                    # List available interfaces
  python cli_sniffer.py --interface eth0          # Capture on eth0
  python cli_sniffer.py -i eth0 -f "tcp port 80" # Capture HTTP traffic
  python cli_sniffer.py -i eth0 -f "host 192.168.1.1" # Capture specific host
        """
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available network interfaces'
    )
    
    parser.add_argument(
        '--interface', '-i',
        type=str,
        help='Network interface to capture on'
    )
    
    parser.add_argument(
        '--filter', '-f',
        type=str,
        default='',
        help='BPF filter string (e.g., "tcp port 80", "host 192.168.1.1")'
    )
    
    parser.add_argument(
        '--max-packets', '-m',
        type=int,
        default=1000,
        help='Maximum packets to store in memory (default: 1000)'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Create sniffer instance
    sniffer = NetworkSniffer()
    
    # List interfaces if requested
    if args.list:
        if not list_interfaces(sniffer):
            sys.exit(1)
        return
    
    # Check if interface is specified
    if not args.interface:
        console.print("[red]Error: Interface must be specified![/red]")
        console.print("Use --list to see available interfaces")
        console.print("Use --help for more information")
        sys.exit(1)
    
    # Validate interface
    interfaces = sniffer.get_available_interfaces()
    if args.interface not in interfaces:
        console.print(f"[red]Error: Interface '{args.interface}' not found![/red]")
        console.print("\nAvailable interfaces:")
        for iface in interfaces:
            console.print(f"  - {iface}")
        sys.exit(1)
    
    # Start live capture
    try:
        live_capture(args.interface, args.filter, args.max_packets)
    except Exception as e:
        console.print(f"[red]Error during capture: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main() 