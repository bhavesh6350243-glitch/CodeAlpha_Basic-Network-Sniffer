#!/usr/bin/env python3
"""
Health Check System for Network Sniffer
Monitors application health and provides diagnostics.
"""

import sys
import os
import platform
import subprocess
import time
from datetime import datetime
from pathlib import Path
from logger import get_logger

logger = get_logger("health_check")

class HealthChecker:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.info = []
        
    def check_python_version(self):
        """Check Python version compatibility"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            self.issues.append(f"Python version {version.major}.{version.minor} is too old. Required: 3.7+")
        else:
            self.info.append(f"Python version {version.major}.{version.minor}.{version.micro} is compatible")
    
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        required_deps = {
            'flask': 'Flask web framework',
            'scapy': 'Packet manipulation library',
            'flask_socketio': 'WebSocket support for Flask',
            'rich': 'Rich terminal output',
            'psutil': 'System and process utilities',
            'colorama': 'Cross-platform colored terminal text'
        }
        
        missing_deps = []
        for dep, description in required_deps.items():
            try:
                __import__(dep)
                self.info.append(f"✓ {dep} ({description})")
            except ImportError:
                missing_deps.append(dep)
                self.issues.append(f"✗ {dep} ({description}) - Missing")
        
        if missing_deps:
            self.warnings.append(f"Missing dependencies: {', '.join(missing_deps)}")
    
    def check_permissions(self):
        """Check if running with appropriate permissions"""
        if os.name == 'nt':  # Windows
            try:
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
                if is_admin:
                    self.info.append("✓ Running with Administrator privileges")
                else:
                    self.warnings.append("⚠ Running without Administrator privileges (packet capture may fail)")
            except:
                self.warnings.append("⚠ Could not determine Administrator status")
        else:  # Unix-like
            is_root = os.geteuid() == 0
            if is_root:
                self.info.append("✓ Running with root privileges")
            else:
                self.warnings.append("⚠ Running without root privileges (packet capture may fail)")
    
    def check_network_interfaces(self):
        """Check for available network interfaces"""
        try:
            from network_sniffer import NetworkSniffer
            sniffer = NetworkSniffer()
            interfaces = sniffer.get_available_interfaces()
            
            if interfaces:
                self.info.append(f"✓ Found {len(interfaces)} network interfaces")
                for interface in interfaces[:3]:  # Show first 3
                    self.info.append(f"  - {interface}")
                if len(interfaces) > 3:
                    self.info.append(f"  ... and {len(interfaces) - 3} more")
            else:
                self.warnings.append("⚠ No network interfaces found")
        except Exception as e:
            self.issues.append(f"✗ Error checking network interfaces: {e}")
    
    def check_file_permissions(self):
        """Check file and directory permissions"""
        current_dir = Path.cwd()
        if current_dir.is_dir():
            self.info.append(f"✓ Working directory: {current_dir}")
        else:
            self.issues.append(f"✗ Invalid working directory: {current_dir}")
        
        # Check if we can create files
        try:
            test_file = current_dir / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            self.info.append("✓ File write permissions OK")
        except Exception as e:
            self.issues.append(f"✗ File write permissions failed: {e}")
    
    def check_ports(self):
        """Check if required ports are available"""
        import socket
        
        ports_to_check = [5000, 5001]  # Web and demo ports
        
        for port in ports_to_check:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    self.info.append(f"✓ Port {port} is available")
            except OSError:
                self.warnings.append(f"⚠ Port {port} is already in use")
    
    def check_system_info(self):
        """Check system information"""
        self.info.append(f"Platform: {platform.system()} {platform.release()}")
        self.info.append(f"Architecture: {platform.machine()}")
        self.info.append(f"Processor: {platform.processor()}")
    
    def check_memory_usage(self):
        """Check available memory"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            self.info.append(f"Total memory: {memory_gb:.1f} GB")
            
            if memory_gb < 2:
                self.warnings.append("⚠ Less than 2GB RAM available - may affect performance")
        except ImportError:
            self.warnings.append("⚠ Could not check memory usage (psutil not available)")
    
    def check_disk_space(self):
        """Check available disk space"""
        try:
            import psutil
            disk = psutil.disk_usage('.')
            free_gb = disk.free / (1024**3)
            self.info.append(f"Free disk space: {free_gb:.1f} GB")
            
            if free_gb < 1:
                self.warnings.append("⚠ Less than 1GB free disk space")
        except ImportError:
            self.warnings.append("⚠ Could not check disk space (psutil not available)")
    
    def run_all_checks(self):
        """Run all health checks"""
        logger.info("Starting health check...")
        
        self.check_python_version()
        self.check_dependencies()
        self.check_permissions()
        self.check_network_interfaces()
        self.check_file_permissions()
        self.check_ports()
        self.check_system_info()
        self.check_memory_usage()
        self.check_disk_space()
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate a health check report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'issues': self.issues,
            'warnings': self.warnings,
            'info': self.info,
            'status': 'healthy' if not self.issues else 'unhealthy'
        }
        
        return report
    
    def print_report(self, report):
        """Print a formatted health check report"""
        print("\n" + "="*60)
        print("🔍 NETWORK SNIFFER HEALTH CHECK")
        print("="*60)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Status: {'🟢 HEALTHY' if report['status'] == 'healthy' else '🔴 UNHEALTHY'}")
        print()
        
        if report['info']:
            print("📋 INFORMATION:")
            for info in report['info']:
                print(f"  {info}")
            print()
        
        if report['warnings']:
            print("⚠️  WARNINGS:")
            for warning in report['warnings']:
                print(f"  {warning}")
            print()
        
        if report['issues']:
            print("❌ ISSUES:")
            for issue in report['issues']:
                print(f"  {issue}")
            print()
        
        print("="*60)
        
        if report['status'] == 'healthy':
            print("✅ System is ready for network monitoring!")
        else:
            print("❌ Please resolve the issues above before proceeding.")
        
        return report['status'] == 'healthy'

def main():
    """Run health check from command line"""
    checker = HealthChecker()
    report = checker.run_all_checks()
    is_healthy = checker.print_report(report)
    
    if is_healthy:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 