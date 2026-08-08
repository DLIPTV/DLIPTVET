#!/usr/bin/env python3
"""SPA server — serves index.html for all routes that don't match a file."""
import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
DIR = os.path.dirname(os.path.abspath(__file__))

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    
    def do_GET(self):
        # If the path doesn't match an existing file, serve index.html
        path = self.translate_path(self.path)
        if not os.path.exists(path) or os.path.isdir(path):
            # Check if it looks like a file request (has extension)
            if '.' not in os.path.basename(self.path.rstrip('/')):
                self.path = '/index.html'
        super().do_GET()

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', PORT), SPAHandler)
    print(f'SPA Server: http://localhost:{PORT}')
    print(f'Serving: {DIR}')
    print('All routes fall back to index.html')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down...')
        server.shutdown()
