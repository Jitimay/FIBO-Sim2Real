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
pip install -q fastapi uvicorn python-multipart python-dotenv pillow numpy requests tqdm pyyaml

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

# Start the API server (subprocess version)
echo "⚙️  Starting API server on http://localhost:8000..."
cd ..
cat > temp_server.py << 'EOF'
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import sys
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class GenerateRequest(BaseModel):
    golden_image_path: str
    count: int

@app.post("/upload-golden-image")
async def upload(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"message": "Uploaded", "path": path}

@app.post("/generate-dataset")
async def generate(request: GenerateRequest):
    try:
        cmd = [
            "bash", "-c", 
            f"cd /home/josh/Kiro/fibo-sim2real-factory && source venv/bin/activate && python scripts/generate_dataset.py --golden_image {request.golden_image_path} --count {request.count}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return {"message": "Dataset generated successfully", "path": "dataset"}
        else:
            return {"message": f"Generation failed: {result.stderr}", "path": None}
            
    except Exception as e:
        return {"message": f"Error: {str(e)}", "path": None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

python temp_server.py &
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
trap "echo '🛑 Stopping servers...'; pkill -f 'python.*server' 2>/dev/null; pkill -f 'http.server' 2>/dev/null; pkill -f 'uvicorn' 2>/dev/null; fuser -k 8000/tcp 2>/dev/null; fuser -k 8080/tcp 2>/dev/null; kill $UI_PID $API_PID 2>/dev/null; rm -f temp_server.py; exit" INT
wait
