#!/usr/bin/env python3
"""
Real-time Security Reconnaissance Automation
Comprehensive web app and API security scanning
"""

import subprocess
import json
import requests
import socket
import ssl
import datetime
from urllib.parse import urlparse
import concurrent.futures
import argparse

class SecurityRecon:
    def __init__(self, target):
        self.target = target
        self.results = {}
        
    def port_scan(self):
        """Quick port scan for common services"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 8080, 8443]
        open_ports = []
        
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
            
        self.results['open_ports'] = open_ports
        return open_ports
    
    def subdomain_enum(self):
        """Basic subdomain enumeration"""
        subdomains = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging']
        found_subdomains = []
        
        for sub in subdomains:
            try:
                full_domain = f"{sub}.{self.target}"
                socket.gethostbyname(full_domain)
                found_subdomains.append(full_domain)
            except socket.gaierror:
                pass
                
        self.results['subdomains'] = found_subdomains
        return found_subdomains
    
    def ssl_check(self):
        """SSL certificate analysis"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.target, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    
            ssl_info = {
                'subject': dict(x[0] for x in cert['subject']),
                'issuer': dict(x[0] for x in cert['issuer']),
                'version': cert['version'],
                'expires': cert['notAfter']
            }
            self.results['ssl_info'] = ssl_info
            return ssl_info
        except Exception as e:
            self.results['ssl_error'] = str(e)
            return None
    
    def web_tech_detection(self):
        """Basic web technology detection"""
        try:
            response = requests.get(f"http://{self.target}", timeout=10)
            headers = response.headers
            
            tech_info = {
                'server': headers.get('Server', 'Unknown'),
                'powered_by': headers.get('X-Powered-By', 'Unknown'),
                'status_code': response.status_code,
                'content_type': headers.get('Content-Type', 'Unknown')
            }
            self.results['web_tech'] = tech_info
            return tech_info
        except Exception as e:
            self.results['web_error'] = str(e)
            return None
    
    def directory_scan(self):
        """Basic directory enumeration"""
        common_dirs = ['admin', 'api', 'backup', 'config', 'test', 'dev', 'uploads']
        found_dirs = []
        
        for directory in common_dirs:
            try:
                url = f"http://{self.target}/{directory}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    found_dirs.append(directory)
            except:
                pass
                
        self.results['directories'] = found_dirs
        return found_dirs
    
    def run_full_scan(self):
        """Execute complete reconnaissance"""
        print(f"Starting recon on {self.target}")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self.port_scan): 'port_scan',
                executor.submit(self.subdomain_enum): 'subdomain_enum',
                executor.submit(self.ssl_check): 'ssl_check',
                executor.submit(self.web_tech_detection): 'web_tech',
                executor.submit(self.directory_scan): 'directory_scan'
            }
            
            for future in concurrent.futures.as_completed(futures):
                scan_type = futures[future]
                try:
                    result = future.result()
                    print(f"✓ {scan_type} completed")
                except Exception as e:
                    print(f"✗ {scan_type} failed: {e}")
        
        return self.results
    
    def generate_report(self):
        """Generate JSON report"""
        report = {
            'target': self.target,
            'timestamp': datetime.datetime.now().isoformat(),
            'results': self.results
        }
        return json.dumps(report, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Security Reconnaissance Tool')
    parser.add_argument('target', help='Target domain or IP')
    parser.add_argument('--output', '-o', help='Output file for results')
    
    args = parser.parse_args()
    
    recon = SecurityRecon(args.target)
    results = recon.run_full_scan()
    report = recon.generate_report()
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)