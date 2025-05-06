import time

from celery import Celery
app = Celery(
   'tasks',
   broker='redis://localhost:6379/0',
   backend='redis://localhost:6379/0'
)
@app.task
def add(x, y):
   return x + y

# celery -A tasks worker
# import os
# import sys
# os.chdir('/Users/veranikalis/Geekbrains/ПРОГРАММИСТ/PYTHON/Flask/m22_queues')
# sys.path.insert(0, os.getcwd())  # <-- ДОБАВИТЬ текущую директорию в sys.path
# from tasks import add
# import os
# import sys
# # Переходим в нужную папку
# os.chdir('/Users/veranikalis/Geekbrains/ПРОГРАММИСТ/PYTHON/Flask/m22_queues')
# # Добавляем текущую папку в список поиска модулей
# sys.path.insert(0, os.getcwd())
# # Теперь можно импортировать
# from tasks import add
# # Отправляем задачу
# result = add.delay(4, 5)
# print(result.get())
# 9

@app.task
def buy_milk(volume: int) -> int:
   print(f'Покупаем {volume} литров молока')
   return volume

@app.task
def buy_bread(count: int) -> int:
   print(f'Покупаем {count} буханок хлеба')
   return count


# ---------

@app.task
def fetch_user_name(id: int) -> str:
   return f'Пётр {id}Первый'

@app.task
def greeting_user(name: str) -> str:
   return f'Здравствуй, {name}!'

@app.task
def heavy_task(n: int) -> int:
   result = 1
   for i in range(2, n):
       result *= i
       time.sleep(0.01)
   return result
