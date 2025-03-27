from flask import Flask
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route("/")
def show_time():
    moscow_time = datetime.now(pytz.timezone("Europe/Moscow")).strftime("%Y-%m-%d %H:%M:%S")
    return f"Точное московское время: {moscow_time}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
