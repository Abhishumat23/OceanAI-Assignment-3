#!/bin/bash

echo "🚀 Starting AI Document Generator Backend..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit backend/.env and add your:"
    echo "   - SECRET_KEY (generate with: openssl rand -hex 32)"
    echo "   - GEMINI_API_KEY (get from: https://makersuite.google.com/app/apikey)"
    echo ""
    echo "Press Enter after you've configured .env..."
    read
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo ""
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
python main.py
