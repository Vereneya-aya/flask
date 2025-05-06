from flask import Flask, request, jsonify
from flask_cors import cross_origin

app = Flask(__name__)

@app.route("/data", methods=["GET", "POST"])
@cross_origin(
    origins=["https://example.com"],
    methods=["GET", "POST"],
    headers=["X-My-Fancy-Header"]
)
def data():
    if request.method == "POST":
        return jsonify({"msg": "Received POST", "data": request.json})
    return jsonify({"msg": "This is GET data"})

if __name__ == "__main__":
    app.run(debug=True)