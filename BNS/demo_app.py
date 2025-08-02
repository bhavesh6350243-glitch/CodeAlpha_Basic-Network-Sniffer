#!/usr/bin/env python3
"""
Demo Network Sniffer Web Application
Flask-based web interface using simulated packet data for testing.
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO, emit
import threading
import time
import json
import os
from datetime import datetime
from demo_sniffer import DemoNetworkSniffer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo_network_sniffer_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global demo sniffer instance
sniffer = DemoNetworkSniffer()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/interfaces')
def get_interfaces():
    """Get available network interfaces"""
    interfaces = sniffer.get_available_interfaces()
    interface_info = []
    
    for interface in interfaces:
        info = sniffer.get_interface_info(interface)
        interface_info.append(info)
    
    return jsonify(interface_info)

@app.route('/api/start_capture', methods=['POST'])
def start_capture():
    """Start packet capture"""
    data = request.get_json()
    interface = data.get('interface')
    filter_str = data.get('filter', '')
    
    if not interface:
        return jsonify({'success': False, 'error': 'Interface not specified'})
    
    success = sniffer.start_capture(interface, filter_str)
    return jsonify({'success': success})

@app.route('/api/stop_capture', methods=['POST'])
def stop_capture():
    """Stop packet capture"""
    success = sniffer.stop_capture()
    return jsonify({'success': success})

@app.route('/api/status')
def get_status():
    """Get current capture status"""
    return jsonify({
        'is_capturing': sniffer.is_capturing,
        'interface': sniffer.interface,
        'filter': sniffer.filter,
        'packet_count': sniffer.packet_count
    })

@app.route('/api/packets')
def get_packets():
    """Get recent packets"""
    count = request.args.get('count', 50, type=int)
    packets = sniffer.get_recent_packets(count)
    return jsonify(packets)

@app.route('/api/stats')
def get_stats():
    """Get packet statistics"""
    stats = sniffer.get_packet_stats()
    return jsonify(stats)

@app.route('/api/clear_packets', methods=['POST'])
def clear_packets():
    """Clear all stored packets"""
    sniffer.clear_packets()
    return jsonify({'success': True})

@app.route('/api/export_packets', methods=['POST'])
def export_packets():
    """Export packets to file"""
    data = request.get_json()
    filename = data.get('filename', f'demo_packets_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    
    success = sniffer.export_packets(filename)
    if success:
        return send_file(filename, as_attachment=True, download_name=filename)
    else:
        return jsonify({'success': False, 'error': 'Export failed'})

def background_packet_emitter():
    """Background thread to emit packet updates via WebSocket"""
    while True:
        if sniffer.is_capturing:
            try:
                # Get new packets from queue
                while not sniffer.packet_queue.empty():
                    packet = sniffer.packet_queue.get_nowait()
                    socketio.emit('new_packet', packet)
                
                # Emit stats periodically
                stats = sniffer.get_packet_stats()
                socketio.emit('stats_update', stats)
                
            except Exception as e:
                print(f"Background emitter error: {e}")
        
        time.sleep(0.1)  # 100ms delay

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Demo client connected')
    emit('status_update', {
        'is_capturing': sniffer.is_capturing,
        'interface': sniffer.interface,
        'packet_count': sniffer.packet_count
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Demo client disconnected')

if __name__ == '__main__':
    # Start background thread for packet emission
    background_thread = threading.Thread(target=background_packet_emitter, daemon=True)
    background_thread.start()
    
    print("Demo Network Sniffer Web Application")
    print("Starting server on http://localhost:5001")
    print("This is a demonstration version with simulated packet data")
    print("Press Ctrl+C to stop")
    
    socketio.run(app, host='0.0.0.0', port=5001, debug=False) 