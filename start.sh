#!/bin/bash

echo "🚀 Starting FIBO-Sim2Real Factory..."

# Kill all existing servers and processes
echo "🛑 Stopping existing servers..."
pkill -f "python.*server" 2>/dev/null
pkill -f "http.server" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null
pkill -f "temp_server" 2>/dev/null
fuser -k 8000/tcp 2>/dev/null
fuser -k 8080/tcp 2>/dev/null
sleep 2

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install minimal dependencies
echo "📦 Installing dependencies..."
pip install -q fastapi uvicorn python-multipart python-dotenv pillow numpy requests tqdm pyyaml ultralytics torch torchvision onnx onnxruntime

# Create test image if it doesn't exist
if [ ! -f "test_image.jpg" ]; then
    echo "🖼️  Creating test image..."
    python3 -c "
from PIL import Image, ImageDraw
img = Image.new('RGB', (512, 512), 'white')
draw = ImageDraw.Draw(img)
draw.ellipse([150, 150, 350, 350], fill='red', outline='darkred', width=3)
draw.ellipse([240, 180, 260, 200], fill='green')
img.save('test_image.jpg', 'JPEG')
"
fi

# Start the UI server
echo "🌐 Starting UI server on http://localhost:8080..."
cd frontend && python3 -m http.server 8080 &
UI_PID=$!

# Start the API server
echo "⚙️  Starting API server on http://localhost:8000 (running main_standalone.py)..."
cd ..
./venv/bin/python run_server.py &
API_PID=$!

echo ""
echo "✅ FIBO-Sim2Real Factory Started!"
echo ""
echo "🌐 Web UI:     http://localhost:8080"
echo "📚 API Docs:   http://localhost:8000/docs"
echo ""
echo "🧪 Test Commands:"
echo "   python scripts/generate_dataset.py --golden_image test_image.jpg --count 10"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt
trap "echo '🛑 Stopping servers...'; kill $UI_PID $API_PID 2>/dev/null; rm -f temp_server.py; exit" INT
wait
