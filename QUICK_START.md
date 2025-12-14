# 🚀 Quick Start Guide

## 1. Setup (2 minutes)
```bash
cd fibo-sim2real-factory
python setup.py
```

## 2. Configure FIBO API
```bash
# Edit .env file
FIBO_API_KEY=your_actual_api_key_here
```

## 3. Start Server
```bash
python run_server.py
```

## 4. Open Web UI
Navigate to: http://localhost:8000

## 5. CLI Usage (Alternative)
```bash
# Generate dataset
python scripts/generate_dataset.py --golden_image sample.jpg --count 1000

# Train model  
python scripts/train_model.py --dataset dataset

# Test on real image
python scripts/test_real.py --image real_test.jpg

# Export for edge
python scripts/export_model.py --model models/fibo_synthetic/weights/best.pt

# Edge inference
python edge-demo/edge_inference.py --model model.onnx --source 0
```

## 6. Project Structure
```
fibo-sim2real-factory/
├── 🌐 frontend/index.html      # Web UI
├── ⚙️  backend/                # FastAPI server
│   ├── main.py                # API endpoints
│   ├── fibo_client.py         # FIBO integration
│   ├── dataset_generator.py   # Synthetic data pipeline
│   └── model_trainer.py       # YOLOv8 training
├── 🛠️  scripts/               # Standalone tools
├── 📱 edge-demo/              # Edge deployment
├── 🤖 ml/                     # ML utilities
└── 📋 README.md               # Full documentation
```

## 7. Demo Flow
1. **Upload** golden image
2. **Generate** 1000+ synthetic variations with FIBO
3. **Train** YOLOv8 model automatically
4. **Test** on real images (Sim2Real validation)
5. **Deploy** to edge devices

## 8. Key Features
✅ JSON-controlled FIBO synthetic data generation  
✅ Automatic labeling and dataset creation  
✅ YOLOv8 training pipeline  
✅ Sim2Real validation  
✅ ONNX export for edge deployment  
✅ Web UI + CLI tools  
✅ Production-ready code  

## 9. Troubleshooting
- **FIBO API errors**: Check API key in .env
- **Training issues**: Ensure dataset was generated successfully
- **Edge deployment**: Install onnxruntime for ONNX models

## 10. Hackathon Ready! 🏆
This project is complete and ready for submission:
- All code is functional and tested
- Comprehensive documentation
- Real Sim2Real pipeline using FIBO
- Production deployment capabilities
