from flask import Flask, request, jsonify, abort
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False  # Отключение CSRF для тестирования

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
        if b == 0:
            abort(400, "Ошибка: на 0 делить нельзя")
        return jsonify({"result": round(a / b, 2)})
    return abort(400, str(form.errors))

# Обработчик ошибок
@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(e):
    return jsonify({"error": "Ошибка: на 0 делить нельзя"}), 400

if __name__ == '__main__':
    app.run(debug=True)
