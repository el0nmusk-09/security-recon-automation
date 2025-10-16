#!/usr/bin/env python3
"""
Real-time Security Monitor
Continuous monitoring with instant alerts
"""

import time
import json
import requests
import hashlib
from datetime import datetime
from recon import SecurityRecon

class RealTimeMonitor:
    def __init__(self, targets, interval=300):  # 5 minute default
        self.targets = targets
        self.interval = interval
        self.baseline = {}
        self.alerts = []
        
    def establish_baseline(self):
        """Create initial baseline for all targets"""
        print("Establishing baseline...")
        for target in self.targets:
            recon = SecurityRecon(target)
            results = recon.run_full_scan()
            self.baseline[target] = {
                'timestamp': datetime.now().isoformat(),
                'results': results,
                'hash': self._hash_results(results)
            }
        print(f"Baseline established for {len(self.targets)} targets")
    
    def _hash_results(self, results):
        """Create hash of results for change detection"""
        return hashlib.md5(json.dumps(results, sort_keys=True).encode()).hexdigest()
    
    def check_changes(self, target):
        """Check for changes against baseline"""
        recon = SecurityRecon(target)
        current_results = recon.run_full_scan()
        current_hash = self._hash_results(current_results)
        
        if target not in self.baseline:
            return None
            
        baseline_hash = self.baseline[target]['hash']
        
        if current_hash != baseline_hash:
            changes = self._detect_specific_changes(
                self.baseline[target]['results'], 
                current_results
            )
            
            alert = {
                'target': target,
                'timestamp': datetime.now().isoformat(),
                'type': 'CHANGE_DETECTED',
                'changes': changes,
                'severity': self._assess_severity(changes)
            }
            
            self.alerts.append(alert)
            self._send_alert(alert)
            
            # Update baseline
            self.baseline[target] = {
                'timestamp': datetime.now().isoformat(),
                'results': current_results,
                'hash': current_hash
            }
            
            return alert
        
        return None
    
    def _detect_specific_changes(self, baseline, current):
        """Detect specific changes between scans"""
        changes = {}
        
        # Check for new open ports
        baseline_ports = set(baseline.get('open_ports', []))
        current_ports = set(current.get('open_ports', []))
        
        new_ports = current_ports - baseline_ports
        closed_ports = baseline_ports - current_ports
        
        if new_ports:
            changes['new_ports'] = list(new_ports)
        if closed_ports:
            changes['closed_ports'] = list(closed_ports)
            
        # Check for new subdomains
        baseline_subs = set(baseline.get('subdomains', []))
        current_subs = set(current.get('subdomains', []))
        
        new_subs = current_subs - baseline_subs
        if new_subs:
            changes['new_subdomains'] = list(new_subs)
            
        # Check for new directories
        baseline_dirs = set(baseline.get('directories', []))
        current_dirs = set(current.get('directories', []))
        
        new_dirs = current_dirs - baseline_dirs
        if new_dirs:
            changes['new_directories'] = list(new_dirs)
            
        return changes
    
    def _assess_severity(self, changes):
        """Assess severity of changes"""
        high_risk_ports = [21, 22, 23, 3389, 5432, 3306]
        
        severity = 'LOW'
        
        if 'new_ports' in changes:
            for port in changes['new_ports']:
                if port in high_risk_ports:
                    severity = 'HIGH'
                    break
            if severity != 'HIGH':
                severity = 'MEDIUM'
                
        if 'new_directories' in changes:
            sensitive_dirs = ['admin', 'backup', 'config', 'test']
            for directory in changes['new_directories']:
                if directory in sensitive_dirs:
                    severity = 'HIGH'
                    break
                    
        return severity
    
    def _send_alert(self, alert):
        """Send alert notification"""
        print(f"🚨 ALERT: {alert['severity']} - {alert['target']}")
        print(f"Changes: {alert['changes']}")
        
        # Here you would integrate with Slack, Discord, email, etc.
        # Example webhook call:
        # requests.post(webhook_url, json=alert)
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        self.establish_baseline()
        
        print(f"Starting real-time monitoring (interval: {self.interval}s)")
        
        while True:
            try:
                for target in self.targets:
                    print(f"Scanning {target}...")
                    alert = self.check_changes(target)
                    
                    if alert:
                        print(f"Changes detected on {target}")
                    else:
                        print(f"No changes on {target}")
                        
                print(f"Waiting {self.interval} seconds...")
                time.sleep(self.interval)
                
            except KeyboardInterrupt:
                print("Monitoring stopped by user")
                break
            except Exception as e:
                print(f"Error during monitoring: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 monitor.py <target1> [target2] ...")
        sys.exit(1)
    
    targets = sys.argv[1:]
    monitor = RealTimeMonitor(targets, interval=300)  # 5 minutes
    monitor.start_monitoring()