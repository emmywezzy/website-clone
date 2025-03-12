import http.server
import socketserver
import os
import webbrowser
from urllib.parse import quote

# Configuration
PORT = 8000
# Look for the website_clone directory in the home directory
DIRECTORY = os.path.expanduser("~/website_clone")  # The directory where the website was cloned

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow resources to load properly
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

def run_server():
    # Make sure the website directory exists
    if not os.path.exists(DIRECTORY):
        print(f"Error: Directory '{DIRECTORY}' not found. Please run clone.py first.")
        return
    
    # Create the server
    handler = MyHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    
    # Get the full URL to open
    url = f"http://localhost:{PORT}/"
    
    print(f"Starting server at http://localhost:{PORT}/")
    print(f"Serving files from: {DIRECTORY}")
    print(f"Opening {url} in your browser...")
    print("Press Ctrl+C to stop the server.")
    
    # Open the browser
    webbrowser.open(url)
    
    # Start the server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    run_server() 