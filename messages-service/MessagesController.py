from http.server import HTTPServer, BaseHTTPRequestHandler


class MessagesController(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Not implemented yet")


server = HTTPServer(("127.0.0.1", 8082), MessagesController)
server.serve_forever()
