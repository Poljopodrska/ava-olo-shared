#!/bin/bash
# Wrapper script for database schema update that loads environment variables

# Set the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load environment variables from .env file
if [ -f "/mnt/c/Users/HP/ava-olo-constitutional/.env" ]; then
    export $(grep -v '^#' /mnt/c/Users/HP/ava-olo-constitutional/.env | xargs)
fi

# Change to script directory
cd "$SCRIPT_DIR"

# Run the Python script
/usr/bin/python3 update_database_schema.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "Schema update completed successfully at $(date)"
else
    echo "Schema update failed at $(date)"
fi