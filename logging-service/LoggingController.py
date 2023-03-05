from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


class LoggingController(BaseHTTPRequestHandler):
    logging = {}

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(str(self.logging).encode()))

    def do_POST(self):
        self.send_response(200)
        content_length = int(self.headers['Content-Length'])
        self.send_header("Content-type", "application/json")
        body = self.rfile.readline(content_length)
        dict_body = urllib.parse.parse_qs(body.decode())
        self.end_headers()
        uuid = list(dict_body.keys())[0]
        msg = list(dict_body.values())[0][0]
        self.logging.update({uuid: msg})
        print("Message: " + uuid + ": " + msg)


server = HTTPServer(("127.0.0.1", 8081), LoggingController)
server.serve_forever()
