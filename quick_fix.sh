#!/bin/bash

echo "🔧 Quick Fix for FIBO API..."

# Kill existing servers
pkill -f "http.server" 2>/dev/null
pkill -f "temp_server" 2>/dev/null
pkill -f "fixed_server" 2>/dev/null

cd /home/josh/Kiro/fibo-sim2real-factory

# Start UI server
echo "🌐 Starting UI server..."
cd frontend && python3 -m http.server 8080 &

# Start fixed API server
echo "⚙️  Starting fixed API server..."
cd .. && source venv/bin/activate && python fixed_server.py &

sleep 2
echo ""
echo "✅ Servers restarted!"
echo "🌐 UI: http://localhost:8080"
echo "📚 API: http://localhost:8000/docs"
echo ""
echo "Now try generating the dataset again in the UI!"
