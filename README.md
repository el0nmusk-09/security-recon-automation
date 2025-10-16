# 🔒 Real-Time Security Reconnaissance Automation

Comprehensive security reconnaissance automation for web applications and APIs with real-time monitoring, change detection, and instant alerting.

## 🚀 Features

### Core Capabilities
- **Real-time Port Scanning** - Monitor open/closed ports continuously
- **Subdomain Enumeration** - Discover new subdomains automatically  
- **SSL Certificate Monitoring** - Track certificate changes and expiry
- **Web Technology Detection** - Identify server technologies and frameworks
- **Directory Discovery** - Find exposed directories and files
- **Change Detection** - Alert on any infrastructure changes
- **Severity Assessment** - Automatic risk scoring of findings

### Monitoring & Alerting
- **Continuous Monitoring** - Configurable scan intervals
- **Real-time Alerts** - Instant notifications via Slack/Discord
- **Web Dashboard** - Live monitoring interface
- **Historical Tracking** - Maintain scan history and trends
- **Baseline Comparison** - Detect deviations from normal state

## 🛠️ Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/el0nmusk-09/security-recon-automation.git
cd security-recon-automation

# Set environment variables
export TARGETS="example.com,api.example.com"
export SLACK_WEBHOOK="your-slack-webhook-url"
export INTERVAL=300  # 5 minutes

# Start monitoring
docker-compose up -d

# Access dashboard
open http://localhost:8080
```

### Option 2: Direct Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run single scan
python3 recon.py example.com --output results.json

# Start real-time monitoring
python3 monitor.py example.com api.example.com

# Start web dashboard
python3 dashboard.py
```

## 📊 Usage Examples

### Single Target Scan
```bash
python3 recon.py example.com
```

### Multiple Target Monitoring
```bash
python3 monitor.py example.com api.example.com admin.example.com
```

### Custom Interval (seconds)
```python
monitor = RealTimeMonitor(['example.com'], interval=60)  # 1 minute
monitor.start_monitoring()
```

## 🔧 Configuration

### Environment Variables
```bash
TARGETS=example.com,api.example.com    # Comma-separated targets
INTERVAL=300                           # Scan interval in seconds
SLACK_WEBHOOK=https://hooks.slack.com/... # Slack notifications
DISCORD_WEBHOOK=https://discord.com/...   # Discord notifications
```

### Alert Severity Levels
- **HIGH**: New high-risk ports (22, 3389, 5432), sensitive directories
- **MEDIUM**: New standard ports, new subdomains
- **LOW**: Minor changes, SSL certificate updates

## 📈 Dashboard Features

Access the web dashboard at `http://localhost:8080`:

- **Live Monitoring** - Real-time scan status
- **Alert Management** - View and acknowledge alerts  
- **Historical Data** - Scan history and trends
- **Target Overview** - Multi-target monitoring
- **Statistics** - Scan counts and severity metrics

## 🔔 Alert Integration

### Slack Integration
```python
# In monitor.py, add your webhook
def _send_alert(self, alert):
    webhook_url = os.getenv('SLACK_WEBHOOK')
    if webhook_url:
        requests.post(webhook_url, json={
            'text': f"🚨 Security Alert: {alert['severity']}",
            'attachments': [{
                'color': 'danger' if alert['severity'] == 'HIGH' else 'warning',
                'fields': [
                    {'title': 'Target', 'value': alert['target'], 'short': True},
                    {'title': 'Changes', 'value': str(alert['changes']), 'short': False}
                ]
            }]
        })
```

## 🛡️ Security Considerations

- **Rate Limiting**: Built-in delays to avoid overwhelming targets
- **Ethical Usage**: Only scan systems you own or have permission to test
- **Data Privacy**: All scan data stored locally by default
- **Network Impact**: Minimal footprint with optimized scanning

## 📋 Scan Components

### Port Scanning
- Common ports: 21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 8080, 8443
- Timeout: 1 second per port
- Concurrent scanning for speed

### Subdomain Enumeration  
- Common subdomains: www, mail, ftp, admin, api, dev, test, staging
- DNS resolution verification
- Expandable wordlist support

### Directory Discovery
- Common directories: admin, api, backup, config, test, dev, uploads
- HTTP status code verification
- Configurable wordlists

### SSL Analysis
- Certificate details extraction
- Expiry date monitoring
- Issuer verification
- Subject information

## 🔄 Continuous Integration

### GitHub Actions Integration
```yaml
name: Security Recon
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  
jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Security Scan
        run: |
          python3 recon.py ${{ secrets.TARGET_DOMAIN }}
          # Upload results to artifacts
```

## 📊 Output Formats

### JSON Report Structure
```json
{
  "target": "example.com",
  "timestamp": "2025-10-16T12:43:00",
  "results": {
    "open_ports": [80, 443, 22],
    "subdomains": ["www.example.com", "api.example.com"],
    "ssl_info": {
      "subject": {"CN": "example.com"},
      "expires": "2025-12-31T23:59:59Z"
    },
    "web_tech": {
      "server": "nginx/1.18.0",
      "powered_by": "PHP/8.0"
    },
    "directories": ["admin", "api"]
  }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and authorized testing purposes only. Users are responsible for complying with applicable laws and obtaining proper authorization before scanning any systems.

---

**Created by**: [Bhindi Security Team](https://bhindi.io)  
**Repository**: https://github.com/el0nmusk-09/security-recon-automation