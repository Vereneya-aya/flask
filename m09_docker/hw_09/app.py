from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def days_until_new_year():
    today = datetime.now()
    new_year = datetime(today.year + 1, 1, 1)
    days_left = (new_year - today).days
    return f"До Нового года осталось {days_left} дней!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)