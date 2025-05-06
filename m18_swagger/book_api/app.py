from flask import Flask
from flask_restful import Api
from flask_apispec import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from resources import BookListResource
import json

app = Flask(__name__)
api = Api(app)

# Регистрируем ресурс
api.add_resource(BookListResource, "/books")

# Конфигурируем спеку
app.config.update({
    'APISPEC_SPEC': APISpec(
        title="Book API",
        version="1.0.0",
        openapi_version="2.0",
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_UI_URL': '/docs/',  # Swagger UI
})

# Документация
docs = FlaskApiSpec(app)
docs.register(BookListResource)

# 👇 ВАЖНО: запуск только если файл запущен напрямую
if __name__ == "__main__":
    # (по желанию) сохраняем спеку в swagger.json
    with open("swagger.json", "w") as f:
        json.dump(app.config['APISPEC_SPEC'].to_dict(), f, indent=2)

    app.run(debug=True)