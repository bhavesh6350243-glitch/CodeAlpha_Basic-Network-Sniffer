#!/usr/bin/env python3
"""
Network Sniffer Startup Script
Provides an easy way to launch the network sniffer application.
"""

import sys
import os
import subprocess
import argparse

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    try:
        import flask
    except ImportError:
        missing_deps.append("flask")
    
    try:
        import scapy
    except ImportError:
        missing_deps.append("scapy")
    
    try:
        import flask_socketio
    except ImportError:
        missing_deps.append("flask-socketio")
    
    try:
        import rich
    except ImportError:
        missing_deps.append("rich")
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies are installed")
        return True

def check_permissions():
    """Check if running with appropriate permissions"""
    if os.name == 'nt':  # Windows
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:  # Unix-like
        return os.geteuid() == 0

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    NETWORK SNIFFER                           ║
    ║                Real-time Packet Analyzer                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def validate_choice(choice):
    """Validate user input choice"""
    try:
        choice_num = int(choice)
        return 1 <= choice_num <= 6
    except ValueError:
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Network Sniffer - Choose your interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start.py --web                    # Launch web interface
  python start.py --cli --list             # List interfaces (CLI)
  python start.py --cli -i eth0            # Start CLI capture
  python start.py --cli -i eth0 -f "tcp port 80"  # HTTP capture
        """
    )
    
    parser.add_argument(
        '--web',
        action='store_true',
        help='Launch web interface'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Launch command line interface'
    )
    
    # CLI-specific arguments
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available interfaces (CLI only)'
    )
    
    parser.add_argument(
        '--interface', '-i',
        type=str,
        help='Network interface to capture on (CLI only)'
    )
    
    parser.add_argument(
        '--filter', '-f',
        type=str,
        default='',
        help='BPF filter string (CLI only)'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Launch demo mode with simulated packet data'
    )
    
    parser.add_argument(
        '--health-check',
        action='store_true',
        help='Run system health check and diagnostics'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Health check option
    if args.health_check:
        print("🔍 Running Health Check...")
        print()
        try:
            from health_check import HealthChecker
            checker = HealthChecker()
            report = checker.run_all_checks()
            is_healthy = checker.print_report(report)
            
            if is_healthy:
                print("\n✅ System is healthy! You can now run the application.")
            else:
                print("\n❌ Please resolve the issues above before running the application.")
                print("💡 Try running in demo mode: python start.py --demo")
            
            sys.exit(0 if is_healthy else 1)
        except ImportError:
            print("❌ Health check module not available")
            print("💡 Make sure health_check.py exists in the current directory")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error running health check: {e}")
            sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 Tip: If you're having trouble with dependencies, try:")
        print("   python -m pip install --upgrade pip")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check permissions
    if not check_permissions():
        print("⚠️  Warning: This application requires administrator/root privileges")
        print("   for packet capture functionality.")
        print("   - Windows: Run Command Prompt as Administrator")
        print("   - Linux/macOS: Use 'sudo python start.py'")
        print("   💡 Demo mode doesn't require privileges!")
        print()
    
    # Determine which interface to launch
    if args.demo:
        print("🎭 Launching Demo Mode...")
        print("   Opening http://localhost:5001")
        print("   This uses simulated packet data for testing")
        print("   Press Ctrl+C to stop")
        print()
        
        try:
            from demo_app import app, socketio
            socketio.run(app, host='0.0.0.0', port=5001, debug=False)
        except KeyboardInterrupt:
            print("\n👋 Demo interface stopped")
        except Exception as e:
            print(f"❌ Error launching demo interface: {e}")
            print("💡 Make sure demo_app.py exists in the current directory")
            sys.exit(1)
    
    elif args.web:
        print("🌐 Launching Web Interface...")
        print("   Opening http://localhost:5000")
        print("   Press Ctrl+C to stop")
        print()
        
        try:
            from app import app, socketio
            socketio.run(app, host='0.0.0.0', port=5000, debug=False)
        except KeyboardInterrupt:
            print("\n👋 Web interface stopped")
        except Exception as e:
            print(f"❌ Error launching web interface: {e}")
            print("💡 Make sure app.py exists in the current directory")
            sys.exit(1)
    
    elif args.cli:
        print("💻 Launching Command Line Interface...")
        print()
        
        # Build CLI command
        cmd = [sys.executable, 'cli_sniffer.py']
        
        if args.list:
            cmd.append('--list')
        elif args.interface:
            cmd.extend(['--interface', args.interface])
            if args.filter:
                cmd.extend(['--filter', args.filter])
        else:
            print("❌ Error: CLI mode requires --list or --interface")
            print("   Use --help for more information")
            sys.exit(1)
        
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n👋 CLI stopped")
        except Exception as e:
            print(f"❌ Error launching CLI: {e}")
            print("💡 Make sure cli_sniffer.py exists in the current directory")
            sys.exit(1)
    
    else:
        # Interactive mode
        print("🎯 Choose your interface:")
        print("   1. Web Interface (Recommended)")
        print("   2. Demo Mode (Simulated Data)")
        print("   3. Command Line Interface")
        print("   4. List Network Interfaces")
        print("   5. Health Check & Diagnostics")
        print("   6. Exit")
        print()
        
        while True:
            try:
                choice = input("Enter your choice (1-6): ").strip()
                
                if not validate_choice(choice):
                    print("❌ Invalid choice. Please enter a number between 1-6.")
                    continue
                
                choice_num = int(choice)
                
                if choice_num == 1:
                    print("\n🌐 Launching Web Interface...")
                    print("   Opening http://localhost:5000")
                    print("   Press Ctrl+C to stop")
                    print()
                    
                    try:
                        from app import app, socketio
                        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
                    except KeyboardInterrupt:
                        print("\n👋 Web interface stopped")
                    except ImportError:
                        print("❌ Error: Could not import app module")
                        print("💡 Make sure app.py exists in the current directory")
                    except Exception as e:
                        print(f"❌ Error launching web interface: {e}")
                    break
                
                elif choice_num == 2:
                    print("\n🎭 Launching Demo Mode...")
                    print("   Opening http://localhost:5001")
                    print("   This uses simulated packet data for testing")
                    print("   Press Ctrl+C to stop")
                    print()
                    
                    try:
                        from demo_app import app, socketio
                        socketio.run(app, host='0.0.0.0', port=5001, debug=False)
                    except KeyboardInterrupt:
                        print("\n👋 Demo interface stopped")
                    except ImportError:
                        print("❌ Error: Could not import demo_app module")
                        print("💡 Make sure demo_app.py exists in the current directory")
                    except Exception as e:
                        print(f"❌ Error launching demo interface: {e}")
                    break
                
                elif choice_num == 3:
                    print("\n💻 Command Line Interface")
                    print("   Use: python cli_sniffer.py --help")
                    print("   Example: python cli_sniffer.py --list")
                    print("   Example: python cli_sniffer.py -i eth0")
                    print()
                    break
                
                elif choice_num == 4:
                    print("\n📋 Listing Network Interfaces...")
                    try:
                        subprocess.run([sys.executable, 'cli_sniffer.py', '--list'])
                    except FileNotFoundError:
                        print("❌ Error: cli_sniffer.py not found")
                        print("💡 Make sure cli_sniffer.py exists in the current directory")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                    print()
                
                elif choice_num == 5:
                    print("\n🔍 Running Health Check & Diagnostics...")
                    print()
                    try:
                        from health_check import HealthChecker
                        checker = HealthChecker()
                        report = checker.run_all_checks()
                        is_healthy = checker.print_report(report)
                        
                        if is_healthy:
                            print("\n✅ System is healthy! You can now run the application.")
                        else:
                            print("\n❌ Please resolve the issues above before running the application.")
                            print("💡 Try running in demo mode: python start.py --demo")
                    except ImportError:
                        print("❌ Health check module not available")
                        print("💡 Make sure health_check.py exists in the current directory")
                    except Exception as e:
                        print(f"❌ Error running health check: {e}")
                    print()
                
                elif choice_num == 6:
                    print("👋 Goodbye!")
                    break
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    main() 