from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import subprocess
import os
import signal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Нужно для FlaskForm


class CodeExecutionForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    timeout = IntegerField('timeout', validators=[DataRequired(), NumberRange(min=1, max=30)])

    class Meta:
        csrf = False  # Отключаем CSRF-защиту


def execute_code(code, timeout):
    try:
        command = ["python3", "-c", code]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   preexec_fn=os.setsid)

        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            return jsonify({"error": "Execution timed out"}), 408

        return jsonify({"stdout": stdout, "stderr": stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/execute', methods=['POST'])
def execute():
    print("Request JSON:", request.json)
    form = CodeExecutionForm(data=request.json)  # Передаём JSON-данные
    print("Received data:", request.json)

    if not form.validate():
        print("Form errors:", form.errors)
        return jsonify({"error": "Invalid input", "details": form.errors}), 400

    return execute_code(form.code.data, form.timeout.data)


if __name__ == '__main__':
    app.run(debug=True, port=8000)