# 🚀 Запуск проекта
#
# Тебе нужно будет запустить:
# 	•	redis-server
# 	•	Flask-приложение (python app.py)
# 	•	Celery worker (celery -A celery_app.celery worker --loglevel=info)
# 	•	Celery beat (celery -A celery_app.celery beat --loglevel=info)
# 	•	Flower (flower -A celery_app.celery --port=5555)


from flask import Flask, request, jsonify
from celery import group
import os
import json
from celery_app import celery
from tasks import blur_image, send_archive

UPLOAD_FOLDER = 'static/uploads'
SUBSCRIBERS_FILE = 'subscribers.json'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/blur', methods=['POST'])
def blur():
    if 'images' not in request.files:
        return jsonify({'error': 'Нет изображений'}), 400

    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'Нет email'}), 400

    files = request.files.getlist('images')
    filenames = []

    for file in files:
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        filenames.append(filename)

    # Группа задач на блюр
    task_group = group(
        blur_image.s(filename)
        for filename in filenames
    )

    # После блюра отправить архив
    result = task_group | send_archive.s(email=email)
    final_result = result.apply_async()

    return jsonify({'group_id': final_result.id}), 202

@app.route('/status/<task_id>', methods=['GET'])
def status(task_id):
    result = celery.AsyncResult(task_id)

    return jsonify({
        'status': result.status,
        'result': result.result
    })

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Нет email'}), 400

    subscribers = []
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, 'r') as f:
            subscribers = json.load(f)

    if email not in subscribers:
        subscribers.append(email)
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump(subscribers, f)

    return jsonify({'message': 'Подписка оформлена'}), 200

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Нет email'}), 400

    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, 'r') as f:
            subscribers = json.load(f)

        if email in subscribers:
            subscribers.remove(email)
            with open(SUBSCRIBERS_FILE, 'w') as f:
                json.dump(subscribers, f)

    return jsonify({'message': 'Подписка отменена'}), 200

if __name__ == '__main__':
    app.run(debug=True)