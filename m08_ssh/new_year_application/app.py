from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

def get_days_until_new_year():
    today = datetime.today()
    new_year = datetime(today.year + 1, 1, 1)
    return (new_year - today).days

@app.route("/")
def home():
    days_left = get_days_until_new_year()
    return render_template("index.html", days_left=days_left)

if __name__ == "__main__":
    app.run(debug=True)