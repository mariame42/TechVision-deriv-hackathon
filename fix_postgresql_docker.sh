#!/bin/bash
# Script to configure PostgreSQL to accept connections from Docker

echo "🔧 Configuring PostgreSQL for Docker connections..."

# Find PostgreSQL config files
PG_CONF=$(find /etc/postgresql -name "postgresql.conf" 2>/dev/null | head -1)
PG_HBA=$(find /etc/postgresql -name "pg_hba.conf" 2>/dev/null | head -1)

if [ -z "$PG_CONF" ] || [ -z "$PG_HBA" ]; then
    echo "❌ PostgreSQL config files not found!"
    exit 1
fi

echo "📁 Found config files:"
echo "   postgresql.conf: $PG_CONF"
echo "   pg_hba.conf: $PG_HBA"

# Backup config files
echo "💾 Backing up config files..."
sudo cp "$PG_CONF" "${PG_CONF}.backup.$(date +%Y%m%d_%H%M%S)"
sudo cp "$PG_HBA" "${PG_HBA}.backup.$(date +%Y%m%d_%H%M%S)"

# Configure postgresql.conf to listen on all interfaces
echo "🔧 Updating postgresql.conf..."
if grep -q "^listen_addresses" "$PG_CONF"; then
    sudo sed -i "s/^listen_addresses.*/listen_addresses = '*'/" "$PG_CONF"
else
    echo "listen_addresses = '*'" | sudo tee -a "$PG_CONF" > /dev/null
fi

# Configure pg_hba.conf to allow Docker network
echo "🔧 Updating pg_hba.conf..."
if ! grep -q "172.17.0.0/16" "$PG_HBA"; then
    echo "host    all    all    172.17.0.0/16    md5" | sudo tee -a "$PG_HBA" > /dev/null
    echo "host    all    all    172.0.0.0/8      md5" | sudo tee -a "$PG_HBA" > /dev/null
fi

# Restart PostgreSQL
echo "🔄 Restarting PostgreSQL..."
sudo systemctl restart postgresql

# Check status
echo "✅ Checking PostgreSQL status..."
sudo systemctl status postgresql --no-pager | head -5

echo ""
echo "✅ Configuration complete!"
echo "📝 PostgreSQL should now accept connections from Docker network (172.17.0.0/16)"
echo ""
echo "🧪 Test connection:"
echo "   docker-compose exec backend python3 -c \"from src.db import get_connection; conn = get_connection(); print('✅ Connected!'); conn.close()\""

