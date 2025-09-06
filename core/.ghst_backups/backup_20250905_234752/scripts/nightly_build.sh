#!/bin/bash
# FANTOM Nightly Build Script for Unix/Linux/macOS
# ⚠️ WARNING: Use at your own risk - No liability assumed!

echo ""
echo "============================================================"
echo "🚀 FANTOM NIGHTLY BUILD - UNIX/LINUX/MACOS"
echo "============================================================"
echo "⚠️ DISCLAIMER: This script assumes NO LIABILITY"
echo "⚠️ Use at your own risk - Verify all outputs"
echo "============================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python not found! Please install Python 3.8+ first."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "🔄 Using $PYTHON_CMD for build process..."

# Check Python version
$PYTHON_CMD --version

# Run the nightly build script
echo "🔄 Starting FANTOM nightly build process..."
$PYTHON_CMD scripts/nightly_build.py

# Check build result
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    echo "📦 Check the dist/ folder for compiled executable"
    echo "📋 See build_report.md for full details"
else
    echo ""
    echo "❌ Build failed! Check the output above for errors."
    echo "📋 Check build_report.md for detailed information."
fi

echo ""
echo "👻 Ghost collective monitoring complete"
echo "⚠️ Remember: Always review AI-generated code before use!"
echo ""