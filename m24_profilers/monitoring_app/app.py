from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Добавляем счётчик вызовов и кодов ответа
@app.route("/hello")
@metrics.counter('endpoint_requests_total', 'Total endpoint requests', labels={'status': lambda r: r.status_code})
def hello():
    return "Hello, Prometheus & Grafana!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


# docker-compose up --build