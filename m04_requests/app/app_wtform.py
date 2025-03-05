from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from typing import Optional
from wtforms.validators import DataRequired, Regexp, Email, NumberRange, ValidationError
from wtforms.validators import Optional as WTOptional
import subprocess
import shlex
import email_validator


app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["WTF_CSRF_ENABLED"] = False


@app.route("/uptime", methods=["GET"])
def uptime():
    command = shlex.split("uptime -p")
    result = subprocess.run(command, capture_output=True, text=True)
    uptime_info = result.stdout.strip()
    return jsonify({"uptime": uptime_info})


@app.route("/ps", methods=["GET"])
def ps():
    args = request.args.getlist('arg')
    safe_args = [shlex.quote(arg) for arg in args]
    command_str = f"ps {' '.join(safe_args)}"
    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True, text=True)
    return f"<pre>{result.stdout}</pre>"


# 📌 Форма регистрации
class RegistrationForm(FlaskForm):
    phone = StringField("Phone", validators=[
        DataRequired(message="Поле phone обязательно для заполнения"),
        Regexp(r"^\d{10}$", message="Телефон должен содержать 10 цифр и только цифры")
    ])
    address = StringField("Address", validators=[
        DataRequired(message="Поле address обязательно для заполнения")
    ])
    name = StringField("Name", validators=[
        DataRequired(message="Поле name обязательно для заполнения"),
        Regexp(r"^[А-ЯЁ][а-яё]+ [А-ЯЁ]\.[А-ЯЁ]\.$", message="Формат: Фамилия И.О.")
    ])
    email = StringField("Email", validators=[
        DataRequired(message="Поле email обязательно для заполнения"),
        Email(message="Некорректный email")
    ])
    index = IntegerField("Index", validators=[
        DataRequired(message="Поле index обязательно для заполнения"),
        NumberRange(min=100000, max=999999, message="Индекс должен содержать 6 цифр")
    ])
    comment = StringField("Comment", validators=[WTOptional()])


@app.route("/register", methods=["POST"])
def register():
    form = RegistrationForm(data=request.json)
    if not form.validate():
        return jsonify({"error": form.errors}), 400
    return jsonify({"message": f"Регистрация успешна, {form.name.data}!"})


# 📌 Форма для проверки счастливого билета
class TicketForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Поле name обязательно для заполнения")
    ])
    family_name = StringField("Family Name", validators=[
        DataRequired(message="Поле family_name обязательно для заполнения")
    ])
    ticket_number = StringField("Ticket Number", validators=[
        DataRequired(message="Поле ticket_number обязательно для заполнения"),
        Regexp(r"^[1-9][0-9]{5}$", message="Номер билета должен быть 6-значным")
    ])


@app.route("/ticket", methods=["POST"])
def check_ticket():
    form = TicketForm(data=request.json)
    if not form.validate():
        return jsonify({"error": form.errors}), 400

    ticket = list(map(int, form.ticket_number.data))
    if sum(ticket[:3]) == sum(ticket[3:]):
        return jsonify({"message": f"Поздравляем вас, {form.name.data} {form.family_name.data}!"})
    return jsonify({"message": "Неудача. Попробуйте ещё раз!"})


if __name__ == "__main__":
    app.run(debug=True)