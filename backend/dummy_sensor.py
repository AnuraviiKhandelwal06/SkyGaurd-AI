from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'temperature': 25.5, 'humidity': 60.0, 'pressure': 1010.0}).encode())

httpd = HTTPServer(('localhost', 9999), SimpleHTTPRequestHandler)
print("Listening on 9999")
httpd.handle_request()
