from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psutil
from datetime import datetime
import json
import os
import threading
import time

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Process Manager Class
class ProcessManager:
    def __init__(self):
        self.whitelist = ["System Idle Process", "System", "explorer.exe", "svchost.exe"]
        self.history_file = "process_history.json"
        self.history = self._load_history()
        
    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-100:], f)  # Keep last 100 entries
    
    def get_all_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu': proc.info['cpu_percent'],
                    'memory': proc.info['memory_percent'],
                    'status': proc.info['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes
    
    def check_threats(self, cpu_threshold=50):
        threats = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['name'] not in self.whitelist and proc.info['cpu_percent'] > cpu_threshold:
                    threats.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu': proc.info['cpu_percent'],
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if threats:
            self.history.extend(threats)
            self._save_history()
        
        return threats
    
    def terminate_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def get_system_stats(self):
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            'running_processes': len(psutil.pids())
        }
    
    def get_history(self):
        return self.history

# Initialize the process manager
manager = ProcessManager()

# Background monitoring thread
def monitor_processes():
    while True:
        manager.check_threats()
        time.sleep(5)

# Start the monitoring thread
monitor_thread = threading.Thread(target=monitor_processes)
monitor_thread.daemon = True
monitor_thread.start()

# API Endpoints
@app.route('/api/processes', methods=['GET'])
def get_processes():
    return jsonify(manager.get_all_processes())

@app.route('/api/threats', methods=['GET'])
def get_threats():
    return jsonify(manager.check_threats())

@app.route('/api/terminate', methods=['POST'])
def terminate_process():
    data = request.json
    if 'pid' not in data:
        return jsonify({'success': False, 'error': 'PID not provided'}), 400
    
    success = manager.terminate_process(data['pid'])
    return jsonify({'success': success})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(manager.get_system_stats())

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(manager.get_history())

# Frontend Serving
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Error Handling
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)