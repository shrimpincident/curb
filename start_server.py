#!/usr/bin/env python3
"""
Simple HTTP server to serve the Curb Your Enthusiasm visualization
"""

import http.server
import socketserver
import webbrowser
import os
import sys

def start_server():
    """Start a simple HTTP server on port 8000"""
    PORT = 8000
    
    # Change to the directory containing the files
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create a simple HTTP request handler
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Create the server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🎭 Curb Your Enthusiasm Episode Visualization Server")
        print(f"📊 Server running at: http://localhost:{PORT}")
        print(f"🌐 Opening visualization in browser...")
        print(f"⏹️  Press Ctrl+C to stop the server")
        
        # Automatically open the browser
        webbrowser.open(f'http://localhost:{PORT}/curb_episodes_visualization.html')
        
        # Start serving files
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            sys.exit(0)

if __name__ == "__main__":
    start_server() 