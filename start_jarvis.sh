#!/bin/bash
# Jarvis Ayurvedic Chatbot - Unix/Linux/macOS Launcher
# Activates virtual environment and launches the application

set -e

echo ""
echo "=========================================================="
echo "  >> JARVIS AYURVEDIC HEALTH ASSISTANT"
echo "=========================================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check and install dependencies
if ! pip show transformers > /dev/null 2>&1; then
    echo ""
    echo "Installing dependencies (this may take a few minutes)..."
    pip install --upgrade pip
    pip install -r requirements_complete.txt
fi

# Run validation
echo ""
echo "Running system validation..."
python validate_system.py

# Launch application
echo ""
echo "Launching Jarvis..."
echo ""
python run_jarvis_improved.py

# Cleanup
deactivate
