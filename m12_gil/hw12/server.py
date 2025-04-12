from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/timestamp/"):
            timestamp = int(self.path.split("/")[-1])
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(date.encode())

if __name__ == "__main__":
    server_address = ("127.0.0.1", 8080)
    httpd = HTTPServer(server_address, SimpleServer)
    print("Сервер запущен на http://127.0.0.1:8080")
    httpd.serve_forever()