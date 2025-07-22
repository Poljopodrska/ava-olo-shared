#!/bin/bash
# Setup automatic database schema updates

echo "🔧 Setting up automatic database schema updates..."

# Make the Python script executable
chmod +x /mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/scripts/update_database_schema.py

# Check if psycopg2 is installed
python3 -c "import psycopg2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing psycopg2..."
    pip3 install psycopg2-binary
fi

# Check if cron is available
if command -v crontab >/dev/null 2>&1; then
    echo "⏰ Setting up cron job..."
    
    # Add cron job (every 30 minutes)
    (crontab -l 2>/dev/null; echo "*/30 * * * * cd /mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/scripts && python3 update_database_schema.py >> /tmp/schema_update.log 2>&1") | crontab -
    
    echo "✅ Cron job added: Database schema will update every 30 minutes"
    echo "📋 View logs: tail -f /tmp/schema_update.log"
    
    # Test the script once
    echo "🧪 Testing schema update script..."
    python3 /mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/scripts/update_database_schema.py
    
else
    echo "⚠️  Cron not available. Manual setup required:"
    echo "   For Windows: Use Task Scheduler"
    echo "   For Linux/Mac: Install cron"
    echo "   Command to run every 30 minutes:"
    echo "   python3 /mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/scripts/update_database_schema.py"
fi

echo "✅ Setup complete!"