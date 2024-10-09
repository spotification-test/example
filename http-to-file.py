import http.server
import socketserver
import os
from pathlib import Path

PORT = 8080  # You can change this to any port you prefer

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the length of the data
        content_length = int(self.headers['Content-Length'])

        # Read the data
        post_data = self.rfile.read(content_length)

        # Create a unique filename
        filename = f"out/request_{self.log_date_time_string().replace(':', '-').replace('/', '_')}.json"

        # Write the data to a file
        with open(filename, 'wb') as file:
            file.write(post_data)

        # Send a simple response back
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'POST data received')

# Set up the server
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    Path('out').mkdir(exist_ok=True)
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
