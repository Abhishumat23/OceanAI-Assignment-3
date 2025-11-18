#!/bin/bash

echo "🚀 Starting AI Document Generator Frontend..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
fi

# Start the dev server
echo ""
echo "✅ Starting React development server on http://localhost:3000"
echo ""
npm run dev
