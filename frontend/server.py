"""
Simple HTTP server to serve the frontend files
"""
import http.server
import socketserver
import os
import webbrowser
import threading
import time

# Set the port for the server
PORT = 8001  # Changed from 8000 to 8001

# Change to the frontend directory
frontend_dir = os.path.join(os.path.dirname(__file__))
os.chdir(frontend_dir)

# Create handler to serve files
Handler = http.server.SimpleHTTPRequestHandler

# Create server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving frontend at http://localhost:{PORT}")
    
    # Open browser in a separate thread after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open(f"http://localhost:{PORT}")
    
    threading.Thread(target=open_browser).start()
    
    try:
        print(f"Server running at http://localhost:{PORT}/")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()