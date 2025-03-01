from flask import Flask
from datetime import datetime

app = Flask(__name__)

WEEKDAYS = ("понедельника", "вторника", "среды", "четверга", "пятницы", "субботы", "воскресенья")

@app.route("/week/<name>")
def weekday(name: str):
    weekday = datetime.today().weekday()
    return {"message": f"Привет, {name}. Хорошей {WEEKDAYS[weekday]}!"}