#!/bin/bash

# ShopifyPulse Startup Script

echo "🚀 Starting ShopifyPulse..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your actual credentials"
fi

# Initialize database
echo "🗄️  Initializing database..."
flask init-db

# Seed sample data
echo "🌱 Seeding sample data..."
flask seed-data

echo ""
echo "✅ ShopifyPulse is ready!"
echo ""
echo "🌐 Open http://localhost:5000 to view the landing page"
echo "📊 Open http://localhost:5000/demo to view the dashboard"
echo ""
echo "Starting server..."
flask run --host=0.0.0.0 --port=5000
