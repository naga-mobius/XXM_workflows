@echo off
REM XXM Workflows Installation Script for Windows
REM This script installs the XXM Workflows package and its dependencies

echo 🚀 Installing XXM Workflows Package...

REM Check if Python 3.8+ is available
echo 📋 Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% detected

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: pip not found. Please install pip and try again.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
pip install --upgrade pip

REM Install the package in development mode
echo 📦 Installing XXM Workflows in development mode...
pip install -e .

REM Install optional dependencies based on user choice
echo.
echo 📚 Optional Dependencies:
echo 1) Development tools (pytest, black, flake8, mypy)
echo 2) Examples (jupyter, notebook)
echo 3) All optional dependencies
echo 4) Skip optional dependencies
echo.
set /p "choice=Choose an option (1-4) [4]: "
if "%choice%"=="" set choice=4

if "%choice%"=="1" (
    echo 🛠️  Installing development dependencies...
    pip install -e ".[dev]"
) else if "%choice%"=="2" (
    echo 📓 Installing example dependencies...
    pip install -e ".[examples]"
) else if "%choice%"=="3" (
    echo 🎯 Installing all dependencies...
    pip install -e ".[full]"
) else (
    echo ⏭️  Skipping optional dependencies
)

REM Install Unsloth (requires special handling)
echo 🦥 Installing Unsloth...
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

echo.
echo 🎉 Installation completed successfully!
echo.
echo 📖 Quick Start:
echo    call venv\Scripts\activate.bat  REM If not already activated
echo    python inference_example.py
echo.
echo 📚 Documentation:
echo    See README.md for detailed usage examples
echo.
echo 🔍 Verify installation:
echo    python -c "from xxm_workflows import LLM, LLMInference; print('✅ Installation verified!')"
echo.
pause