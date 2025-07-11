#!/bin/bash
# Labubu Pilot Runner Script
# This script sets up the environment and runs the bot

echo "🤖 Starting Labubu Pilot..."
echo "=" * 50

# Activate virtual environment
source venv/bin/activate

# Set PATH to use the correct ChromeDriver
export PATH="/opt/homebrew/bin:$PATH"

# Run the bot
python labubu_bot.py 