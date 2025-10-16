#!/bin/bash

# 🔒 Security Recon Automation - Quick Deploy Script
# Automated setup for real-time security reconnaissance

set -e

echo "🔒 Security Recon Automation Setup"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Get target domains from user
echo "📋 Enter target domains to monitor (comma-separated):"
read -p "Targets: " TARGETS

if [ -z "$TARGETS" ]; then
    echo "❌ No targets specified. Exiting."
    exit 1
fi

# Get scan interval
echo "⏱️  Enter scan interval in seconds (default: 300):"
read -p "Interval: " INTERVAL
INTERVAL=${INTERVAL:-300}

# Get notification webhooks (optional)
echo "🔔 Enter Slack webhook URL (optional, press Enter to skip):"
read -p "Slack Webhook: " SLACK_WEBHOOK

echo "🔔 Enter Discord webhook URL (optional, press Enter to skip):"
read -p "Discord Webhook: " DISCORD_WEBHOOK

# Create environment file
cat > .env << EOF
TARGETS=$TARGETS
INTERVAL=$INTERVAL
SLACK_WEBHOOK=$SLACK_WEBHOOK
DISCORD_WEBHOOK=$DISCORD_WEBHOOK
EOF

echo "✅ Environment configured"

# Create data directory
mkdir -p data config

echo "📁 Directories created"

# Build and start containers
echo "🐳 Building Docker containers..."
docker-compose build

echo "🚀 Starting security monitoring..."
docker-compose up -d

# Wait for services to start
sleep 5

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Security monitoring started successfully!"
    echo ""
    echo "📊 Dashboard: http://localhost:8080"
    echo "🔍 Monitoring targets: $TARGETS"
    echo "⏱️  Scan interval: ${INTERVAL}s"
    echo ""
    echo "📋 Useful commands:"
    echo "  View logs:     docker-compose logs -f"
    echo "  Stop monitor:  docker-compose down"
    echo "  Restart:       docker-compose restart"
    echo ""
    echo "🔔 Alerts will be sent to configured webhooks"
else
    echo "❌ Failed to start services. Check logs:"
    docker-compose logs
    exit 1
fi