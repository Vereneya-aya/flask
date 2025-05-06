# server.py
from flask import Flask, jsonify
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"})

# Включаем поддержку HTTP/1.1 для Keep-Alive
# WSGIRequestHandler.protocol_version = "HTTP/1.1"

if __name__ == '__main__':
    app.run(debug=True)