#!/bin/bash
# Chronos Outreach System - Quick Launcher

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}CHRONOS OUTREACH SYSTEM${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import anthropic" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

# Check if config exists
if [ ! -f "config.json" ]; then
    echo ""
    echo "Configuration file not found."
    echo "Running setup wizard..."
    echo ""
    python setup.py setup
fi

# Main menu
echo ""
echo "What would you like to do?"
echo ""
echo "1. Research brands in a category"
echo "2. Generate email sequences"
echo "3. Launch web interface (review & send)"
echo "4. View statistics"
echo "5. Run setup wizard"
echo "6. Exit"
echo ""

read -p "Choose option (1-6): " choice

case $choice in
    1)
        read -p "Enter category (e.g., 'Irish Whiskey'): " category
        read -p "How many brands? (default 20): " limit
        limit=${limit:-20}
        python main.py research --category "$category" --limit $limit
        ;;
    2)
        python main.py generate
        ;;
    3)
        python main.py review
        ;;
    4)
        python main.py stats
        ;;
    5)
        python setup.py setup
        ;;
    6)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid option"
        ;;
esac
