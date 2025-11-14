#!/bin/bash
# Chronos Outreach System - Web Interface Launcher

echo "🚀 Starting Chronos Outreach Web Interface..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Check if config exists
if [ ! -f "config.json" ]; then
    echo "⚙️ Configuration not found. Running setup..."
    python setup.py
fi

# Launch the web interface
echo ""
echo "🌐 Launching web interface..."
echo "🔗 The app will open at: http://localhost:8501"
echo "👉 Press Ctrl+C to stop the server"
echo ""

streamlit run app.py --server.headless=true
