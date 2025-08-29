#!/bin/bash

# XXM Workflows Installation Script
# This script installs the XXM Workflows package and its dependencies

set -e  # Exit on any error

echo "🚀 Installing XXM Workflows Package..."

# Check if Python 3.8+ is available
echo "📋 Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Error: Python 3.8+ required. Found Python $PYTHON_VERSION"
    echo "   Please install Python 3.8 or higher and try again."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ Error: pip not found. Please install pip and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode
echo "📦 Installing XXM Workflows in development mode..."
pip install -e .

# Install optional dependencies based on user choice
echo ""
echo "📚 Optional Dependencies:"
echo "1) Development tools (pytest, black, flake8, mypy)"
echo "2) Examples (jupyter, notebook)"
echo "3) All optional dependencies"
echo "4) Skip optional dependencies"
echo ""
read -p "Choose an option (1-4) [4]: " choice
choice=${choice:-4}

case $choice in
    1)
        echo "🛠️  Installing development dependencies..."
        pip install -e ".[dev]"
        ;;
    2)
        echo "📓 Installing example dependencies..."
        pip install -e ".[examples]"
        ;;
    3)
        echo "🎯 Installing all dependencies..."
        pip install -e ".[full]"
        ;;
    4)
        echo "⏭️  Skipping optional dependencies"
        ;;
    *)
        echo "⚠️  Invalid choice. Skipping optional dependencies."
        ;;
esac

# Install Unsloth (requires special handling)
echo "🦥 Installing Unsloth..."
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📖 Quick Start:"
echo "   source venv/bin/activate  # If not already activated"
echo "   python inference_example.py"
echo ""
echo "📚 Documentation:"
echo "   See README.md for detailed usage examples"
echo ""
echo "🔍 Verify installation:"
echo "   python -c \"from xxm_workflows import LLM, LLMInference; print('✅ Installation verified!')\""