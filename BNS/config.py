#!/usr/bin/env python3
"""
Configuration file for Network Sniffer
Centralized settings for the application.
"""

import os
from pathlib import Path

# Application settings
APP_NAME = "Network Sniffer"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Real-time Packet Analyzer"

# Web interface settings
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
DEMO_PORT = 5001
DEBUG_MODE = False

# Packet capture settings
MAX_PACKETS_IN_MEMORY = 1000
PACKET_CAPTURE_TIMEOUT = 30  # seconds
DEFAULT_FILTER = ""

# File export settings
EXPORT_DIR = "exports"
DEFAULT_EXPORT_FORMAT = "json"

# Interface settings
DEFAULT_INTERFACE = None
AUTO_DETECT_INTERFACES = True

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = "network_sniffer.log"

# Security settings
SECRET_KEY = "network_sniffer_secret_key_2024"
CORS_ALLOWED_ORIGINS = "*"

# Performance settings
WEBSOCKET_PING_INTERVAL = 25
WEBSOCKET_PING_TIMEOUT = 10
BACKGROUND_TASK_INTERVAL = 1  # seconds

# Demo mode settings
DEMO_PACKET_INTERVAL_MIN = 0.1  # seconds
DEMO_PACKET_INTERVAL_MAX = 2.0  # seconds
DEMO_PACKET_COUNT = 100

# Supported protocols for analysis
SUPPORTED_PROTOCOLS = [
    'TCP', 'UDP', 'ICMP', 'ARP', 'HTTP', 'HTTPS', 
    'DNS', 'DHCP', 'SSH', 'FTP', 'SMTP', 'POP3'
]

# Common BPF filters
COMMON_FILTERS = {
    "HTTP Traffic": "tcp port 80",
    "HTTPS Traffic": "tcp port 443",
    "DNS Queries": "udp port 53",
    "SSH Traffic": "tcp port 22",
    "ICMP (Ping)": "icmp",
    "ARP Traffic": "arp",
    "All TCP": "tcp",
    "All UDP": "udp"
}

def get_export_path():
    """Get the export directory path, create if it doesn't exist"""
    export_path = Path(EXPORT_DIR)
    export_path.mkdir(exist_ok=True)
    return export_path

def get_log_path():
    """Get the log file path"""
    return Path(LOG_FILE)

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if WEB_PORT < 1 or WEB_PORT > 65535:
        errors.append("WEB_PORT must be between 1 and 65535")
    
    if DEMO_PORT < 1 or DEMO_PORT > 65535:
        errors.append("DEMO_PORT must be between 1 and 65535")
    
    if WEB_PORT == DEMO_PORT:
        errors.append("WEB_PORT and DEMO_PORT must be different")
    
    if MAX_PACKETS_IN_MEMORY < 1:
        errors.append("MAX_PACKETS_IN_MEMORY must be at least 1")
    
    if PACKET_CAPTURE_TIMEOUT < 1:
        errors.append("PACKET_CAPTURE_TIMEOUT must be at least 1 second")
    
    return errors

def load_from_env():
    """Load configuration from environment variables"""
    global WEB_PORT, DEMO_PORT, DEBUG_MODE, MAX_PACKETS_IN_MEMORY
    
    WEB_PORT = int(os.getenv('WEB_PORT', WEB_PORT))
    DEMO_PORT = int(os.getenv('DEMO_PORT', DEMO_PORT))
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    MAX_PACKETS_IN_MEMORY = int(os.getenv('MAX_PACKETS_IN_MEMORY', MAX_PACKETS_IN_MEMORY))

# Load environment variables
load_from_env()

# Validate configuration
config_errors = validate_config()
if config_errors:
    print("Configuration errors:")
    for error in config_errors:
        print(f"  - {error}")
    raise ValueError("Invalid configuration") 