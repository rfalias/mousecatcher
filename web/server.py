import http.server
import socketserver
#ChatGPT generated most of this

PORT = 9999

def generate_content():
    with open('/root/mousecatcher/web/data', 'r') as f:
        return f.read()

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        content = generate_content()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(content.encode())

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.allow_reuse_address = True
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer is stopping...")
    finally:
        httpd.server_close()
        print("Server has been shut down.")
