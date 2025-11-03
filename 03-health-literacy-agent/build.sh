#!/usr/bin/env bash

echo "🚀 Starting HealthLiteracy AI deployment..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Setting up static files..."
python manage.py collectstatic --noinput --clear

# Run database migrations (if DB is added later)
# echo "🗃️ Running migrations..."
# python manage.py migrate

echo "✅ Build completed successfully!"