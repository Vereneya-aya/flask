import random

from flask import Flask, request, jsonify
from celery import Celery, group
import time

app = Flask(__name__)

# Конфигурация Celery
celery = Celery(
   app.name,
   broker='redis://localhost:6379/0',
   backend='redis://localhost:6379/0',
)

# Задача Celery для обработки изображения
@celery.task
def process_image(image_id: str):
   # В реальной ситуации здесь может быть обработка изображения
   # В данном примере просто делаем задержку для демонстрации
   time.sleep(random.randint(5, 15))
   return f'Image {image_id} processed'

@app.route('/process_images', methods=['POST'])
def process_images():
   images = request.json.get('images')

   if images and isinstance(images, list):
       # Создаём группу задач
       task_group = group(
           process_image.s(image_id)
           for image_id in images
       )

       # Запускаем группу задач и сохраняем её
       result = task_group.apply_async()
       result.save()

       # Возвращаем пользователю ID группы для отслеживания
       return jsonify({'group_id': result.id}), 202
   else:
       return jsonify({'error': 'Missing or invalid images parameter'}), 400

@app.route('/status/<group_id>', methods=['GET'])
def get_group_status(group_id: str):
   result = celery.GroupResult.restore(group_id)

   if result:
       # Если группа с таким ID существует,
       # возвращаем долю выполненных задач
       status = result.completed_count() / len(result)
       return jsonify({'status': status}), 200
   else:
       # Иначе возвращаем ошибку
       return jsonify({'error': 'Invalid group_id'}), 404

@app.route('/cancel/<group_id>', methods=['POST'])
def cancel_group(group_id: str):
    result = celery.GroupResult.restore(group_id)
    if result:
        for task in result.children:
            if task:
                celery.control.revoke(task.id, terminate=True)
        return jsonify({'message': f'Group {group_id} canceled'}), 200
    else:
        return jsonify({'error': 'Invalid group_id'}), 404

import time as time_module  # чтобы не конфликтовать с time.sleep
from functools import lru_cache

# Глобальные переменные для кэширования
_last_control_info = None
_last_control_time = 0

@app.route('/control', methods=['GET'])
def control_info():
    global _last_control_info, _last_control_time

    now = time_module.time()
    if _last_control_info is None or (now - _last_control_time > 10):
        inspect = celery.control.inspect()

        _last_control_info = {
            'active': inspect.active(),
            'reserved': inspect.reserved(),
            'scheduled': inspect.scheduled(),
        }
        _last_control_time = now

    return jsonify(_last_control_info), 200

if __name__ == '__main__':
   app.run(debug=True)



# docker run -p 6379:6379 --name my-redis -d redis

# celery -A app.celery worker --loglevel=info