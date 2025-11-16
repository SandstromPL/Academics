#!/bin/bash
# Setup script for the warehouse robot simulator

echo "======================================================================"
echo "  Setting up Multi-Agent Warehouse Robot Simulator"
echo "======================================================================"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Virtual environment created!"
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "======================================================================"
echo "  ✅ Setup Complete!"
echo "======================================================================"
echo ""
echo "To use the simulator:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the simulator:"
echo "   python main.py"
echo ""
echo "3. Or run demos:"
echo "   python demo.py"
echo ""
echo "4. Or run tests:"
echo "   python test_components.py"
echo ""
echo "5. When done, deactivate:"
echo "   deactivate"
echo ""
echo "======================================================================"
