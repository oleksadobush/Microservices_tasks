from http.server import HTTPServer, BaseHTTPRequestHandler
import uuid
import json
import requests

logging_url = "http://127.0.0.1:8081/logging-service"
message_url = "http://127.0.0.1:8082/message-service"


class FacadeController(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/facade-service':
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            response_log = requests.get(logging_url)
            response_log = response_log.text.replace("\'", "\"")
            response_log = json.loads(response_log)
            response_mes = requests.get(message_url).text
            self.wfile.write(bytes(str(list(response_log.values())).encode()))
            self.wfile.write(bytes(str("\n").encode()))
            self.wfile.write(bytes(str(response_mes).encode()))

    def do_POST(self):
        if self.path == '/facade-service':
            self.send_response(200)
            content_length = int(self.headers['Content-Length'])
            self.send_header("Content-type", "application/json")
            body = json.loads(self.rfile.read(content_length))
            new_uuid = uuid.uuid4()
            self.end_headers()
            msg = dict()
            msg[str(new_uuid)] = list(body.values())[0]
            requests.post(logging_url, data=msg)


server = HTTPServer(("127.0.0.1", 8080), FacadeController)
server.serve_forever()
