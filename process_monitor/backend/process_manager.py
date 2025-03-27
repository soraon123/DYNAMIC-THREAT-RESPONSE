import psutil
import time
from datetime import datetime
import json
import os

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