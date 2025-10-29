#!/bin/bash

# XAUUSD Chart Application Startup Script
echo "🚀 Starting XAUUSD Chart Application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing JavaScript dependencies..."
    npm install
fi

echo ""
echo "✅ Setup completed!"
echo ""
echo "🌐 Starting Flask server..."
echo "   Access the application at: http://localhost:5000"
echo "   API endpoint example: http://localhost:5000/api/ohlc/XAUUSD/H1"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Flask server
python api.py