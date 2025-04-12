from flask import Flask, request, jsonify

app = Flask(__name__)

rooms = [
    {"roomId": 1, "floor": 2, "guestNum": 1, "beds": 1, "price": 2000},
    {"roomId": 2, "floor": 1, "guestNum": 2, "beds": 1, "price": 2500},
]

@app.route('/')
def index():
    return 'API is running!'

@app.route('/get-room', methods=['GET'])
def get_room():
    return jsonify({"rooms": rooms}), 200

@app.route('/add-room', methods=['POST'])
def add_room():
    new_room = request.json
    rooms.append(new_room)
    return jsonify({"rooms": rooms}), 200

@app.route('/booking', methods=['POST'])
def booking():
    data = request.json
    room_id = data.get("roomId")
    global rooms
    rooms = [room for room in rooms if room["roomId"] != room_id]
    return jsonify({"message": "Room booked"}), 200

@app.route('/test', methods=['POST'])
def test():
    return jsonify({"rooms": rooms}), 200

if __name__ == '__main__':
    app.run(debug=True)