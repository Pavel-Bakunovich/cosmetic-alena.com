#!/bin/bash
# Quick start script for Cosmetic Alena Flask Application

set -e

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║     Cosmetic Alena - Flask Website Application Setup              ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# Install requirements
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << 'EOF'
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=cosmetic-alena-dev-key-change-in-production
EOF
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                   Setup Complete! 🎉                              ║"
echo "╠════════════════════════════════════════════════════════════════════╣"
echo "║                                                                    ║"
echo "║  To start the development server, run:                            ║"
echo "║                                                                    ║"
echo "║      python3 app.py                                              ║"
echo "║                                                                    ║"
echo "║  Then open your browser and visit:                               ║"
echo "║                                                                    ║"
echo "║      http://localhost:5000                                       ║"
echo "║                                                                    ║"
echo "╠════════════════════════════════════════════════════════════════════╣"
echo "║  Project Documentation: See SETUP_AND_RUN.md                      ║"
echo "║  API Endpoints: See app.py for all available routes               ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
