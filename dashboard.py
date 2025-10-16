#!/usr/bin/env python3
"""
Real-time Security Dashboard
Web interface for monitoring security scans
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

class SecurityDashboard:
    def __init__(self):
        self.db_path = '/app/data/security.db'
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                results TEXT NOT NULL,
                severity TEXT DEFAULT 'LOW'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                changes TEXT NOT NULL,
                severity TEXT NOT NULL,
                acknowledged BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_recent_scans(self, hours=24):
        """Get recent scans from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        cursor.execute('''
            SELECT target, timestamp, results, severity 
            FROM scans 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC
        ''', (since,))
        
        scans = cursor.fetchall()
        conn.close()
        
        return [
            {
                'target': scan[0],
                'timestamp': scan[1],
                'results': json.loads(scan[2]),
                'severity': scan[3]
            }
            for scan in scans
        ]
    
    def get_active_alerts(self):
        """Get unacknowledged alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, target, timestamp, alert_type, changes, severity 
            FROM alerts 
            WHERE acknowledged = FALSE 
            ORDER BY timestamp DESC
        ''')
        
        alerts = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': alert[0],
                'target': alert[1],
                'timestamp': alert[2],
                'type': alert[3],
                'changes': json.loads(alert[4]),
                'severity': alert[5]
            }
            for alert in alerts
        ]

dashboard = SecurityDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/scans')
def api_scans():
    """API endpoint for recent scans"""
    hours = request.args.get('hours', 24, type=int)
    scans = dashboard.get_recent_scans(hours)
    return jsonify(scans)

@app.route('/api/alerts')
def api_alerts():
    """API endpoint for active alerts"""
    alerts = dashboard.get_active_alerts()
    return jsonify(alerts)

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    scans = dashboard.get_recent_scans(24)
    alerts = dashboard.get_active_alerts()
    
    stats = {
        'total_scans_24h': len(scans),
        'active_alerts': len(alerts),
        'high_severity_alerts': len([a for a in alerts if a['severity'] == 'HIGH']),
        'targets_monitored': len(set(scan['target'] for scan in scans))
    }
    
    return jsonify(stats)

@app.route('/api/acknowledge/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    conn = sqlite3.connect(dashboard.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE alerts 
        SET acknowledged = TRUE 
        WHERE id = ?
    ''', (alert_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    app.run(host='0.0.0.0', port=8080, debug=True)