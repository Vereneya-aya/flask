from flask import Flask
from flask_jsonrpc import JSONRPC
from flasgger import Swagger, swag_from

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
swagger = Swagger(app)

# Метод: Сложение
@jsonrpc.method('Calculator.add')
@swag_from({
    'tags': ['Calculator'],
    'parameters': [
        {'name': 'a', 'in': 'formData', 'type': 'number', 'required': True},
        {'name': 'b', 'in': 'formData', 'type': 'number', 'required': True},
    ],
    'responses': {
        200: {
            'description': 'Сумма двух чисел',
            'schema': {'type': 'number'}
        }
    }
})
def add(a: float, b: float) -> float:
    return a + b

# Метод: Вычитание
@jsonrpc.method('Calculator.subtract')
def subtract(a: float, b: float) -> float:
    return a - b

# Метод: Умножение
@jsonrpc.method('Calculator.multiply')
def multiply(a: float, b: float) -> float:
    return a * b

# Метод: Деление
@jsonrpc.method('Calculator.divide')
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Деление на ноль запрещено.")
    return a / b

if __name__ == '__main__':
    app.run(debug=True)