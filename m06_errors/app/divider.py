import logging
from flask import Flask, request, jsonify, abort
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False  # Отключение CSRF для тестирования

# Настраиваем логгер
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # INFO и выше

# Создаём обработчик для записи в файл stderr.txt
file_handler = logging.FileHandler("fixtures/stderr.txt")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
file_handler.setFormatter(formatter)

# Добавляем обработчик в логгер
logger.addHandler(file_handler)

# Определяем форму
class DivideForm(FlaskForm):
    a = IntegerField('A', validators=[InputRequired()])
    b = IntegerField('B', validators=[InputRequired()])


@app.route('/divide', methods=['POST'])
def divide():
    form = DivideForm(request.form)
    if form.validate_on_submit():
        a = form.a.data
        b = form.b.data

        logger.debug(f"Получены данные: a={a}, b={b}")

        if b == 0:
            logger.warning("Попытка деления на ноль")
            abort(400, "Ошибка: на 0 делить нельзя")

        result = round(a / b, 2)
        logger.info(f"Успешное деление: {a} / {b} = {result}")
        return jsonify({"result": result})

    logger.error(f"Ошибка валидации формы: {form.errors}")
    return abort(400, str(form.errors))


# Обработчик ошибок
@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(e):
    logger.error("Обнаружено деление на ноль")
    return jsonify({"error": "Ошибка: на 0 делить нельзя"}), 400


if __name__ == '__main__':
    logger.info("Запуск приложения Flask")
    app.run(debug=True)


# curl -X POST -d "a=10&b=2" http://127.0.0.1:5000/divide
