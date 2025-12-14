# 🎬 Demo Video Script (3 minutes)

## Scene 1: Problem Statement (30 seconds)
**Narrator:** "Computer vision models need thousands of labeled images. Collecting and labeling real-world data is expensive and time-consuming. What if we could generate perfect synthetic training data instead?"

**Show:** 
- Split screen: expensive manual labeling vs. FIBO synthetic generation
- Cost comparison chart

## Scene 2: FIBO Synthetic Data Generation (60 seconds)
**Narrator:** "Meet FIBO-Sim2Real Factory. Upload one golden image, and FIBO generates 1000+ variations with JSON-controlled parameters."

**Show:**
1. Upload golden image (apple/product/defect)
2. FIBO parameter controls:
   - Camera: azimuth, elevation, distance
   - Lighting: color, angle, intensity
   - Materials: roughness, metallic
   - Backgrounds: industrial, lab, outdoor
3. Generated dataset preview

**Code snippet:**
```json
{
  "camera": {"azimuth": 45, "elevation": 30},
  "lighting": {"intensity": 1.2, "color": [1.0, 0.9, 0.8]},
  "background": "industrial"
}
```

## Scene 3: Training Pipeline (45 seconds)
**Narrator:** "Every synthetic image is automatically labeled. Train YOLOv8 directly on synthetic data - no manual annotation needed."

**Show:**
1. Auto-generated YOLO labels
2. Training metrics dashboard
3. Model convergence graphs

## Scene 4: Sim2Real Validation (30 seconds)
**Narrator:** "The real test: does our synthetic-trained model work on real images?"

**Show:**
1. Test on real photos
2. Detection results with confidence scores
3. Side-by-side: synthetic vs. real performance

## Scene 5: Edge Deployment (15 seconds)
**Narrator:** "Deploy instantly to edge devices. ONNX export for Raspberry Pi and Jetson Nano."

**Show:**
1. Model export to ONNX
2. Live inference on edge device
3. Real-time detection demo

## Closing (10 seconds)
**Narrator:** "FIBO-Sim2Real Factory: From one image to production-ready AI in minutes."

**Show:**
- GitHub repo
- "Built with FIBO" logo
- Hackathon submission ready

---

## Key Talking Points:
- **FIBO is essential** for deterministic, JSON-controlled synthetic data
- **Complete pipeline** from golden image to edge deployment  
- **Real working code** - not just a concept
- **Solves actual problems** in robotics and computer vision
- **Production ready** with proper error handling and documentation
