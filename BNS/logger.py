#!/usr/bin/env python3
"""
Logging system for Network Sniffer
Provides centralized logging functionality.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from config import LOG_LEVEL, LOG_FILE

def setup_logger(name="network_sniffer", level=None):
    """Setup and configure logger"""
    if level is None:
        level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    try:
        log_path = Path(LOG_FILE)
        log_path.parent.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not setup file logging: {e}")
    
    return logger

def log_packet_capture(logger, interface, filter_str, packet_count):
    """Log packet capture events"""
    logger.info(f"Packet capture started - Interface: {interface}, Filter: '{filter_str}', Packets: {packet_count}")

def log_error(logger, error, context=""):
    """Log errors with context"""
    if context:
        logger.error(f"{context}: {error}")
    else:
        logger.error(f"Error: {error}")

def log_performance(logger, operation, duration):
    """Log performance metrics"""
    logger.info(f"Performance - {operation}: {duration:.3f}s")

def log_security(logger, event, details=""):
    """Log security-related events"""
    if details:
        logger.warning(f"Security - {event}: {details}")
    else:
        logger.warning(f"Security - {event}")

def log_interface_detection(logger, interfaces_found, method_used):
    """Log interface detection results"""
    logger.info(f"Interface detection - Found {len(interfaces_found)} interfaces using {method_used}")

def log_web_request(logger, endpoint, status_code, duration=None):
    """Log web interface requests"""
    if duration:
        logger.info(f"Web request - {endpoint}: {status_code} ({duration:.3f}s)")
    else:
        logger.info(f"Web request - {endpoint}: {status_code}")

def log_export(logger, filename, packet_count):
    """Log export operations"""
    logger.info(f"Export - {filename}: {packet_count} packets exported")

def log_demo_mode(logger, enabled=True):
    """Log demo mode status"""
    if enabled:
        logger.info("Demo mode enabled - Using simulated packet data")
    else:
        logger.info("Demo mode disabled - Using real packet capture")

# Create default logger instance
default_logger = setup_logger()

def get_logger(name=None):
    """Get logger instance"""
    if name:
        return logging.getLogger(name)
    return default_logger 