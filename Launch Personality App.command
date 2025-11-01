#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to the app directory
cd "$SCRIPT_DIR"

# Activate the virtual environment
source ./personality_app_env/bin/activate

# Start streamlit with auto-open browser
echo "Starting Personality Assessment App..."
echo "The app will open automatically in your browser."
echo "Close this terminal window to stop the app."

streamlit run personality_app.py --server.port 8508 --server.headless false

# Keep terminal open
read -p "Press any key to exit..."