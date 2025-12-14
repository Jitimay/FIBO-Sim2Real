#!/usr/bin/env python3
import http.server
import socketserver
import json
import subprocess
import os
from urllib.parse import urlparse, parse_qs
import cgi

class UIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/generate-dataset':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Run the CLI command
            cmd = f"cd /home/josh/Kiro/fibo-sim2real-factory && source venv/bin/activate && python scripts/generate_dataset.py --golden_image {data['golden_image_path']} --count {data['count']}"
            
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    response = {"message": "Dataset generated successfully", "path": "dataset"}
                else:
                    response = {"message": f"Generation failed: {result.stderr}", "path": None}
                    
            except Exception as e:
                response = {"message": f"Error: {str(e)}", "path": None}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

os.chdir('/home/josh/Kiro/fibo-sim2real-factory/frontend')
with socketserver.TCPServer(("", 8080), UIHandler) as httpd:
    print("🌐 UI Server running on http://localhost:8080")
    print("✅ FIBO generation will work through CLI calls")
    httpd.serve_forever()
