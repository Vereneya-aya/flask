from random import random

from celery import Celery
from celery.schedules import crontab

app = Celery(
   'tasks',
   broker='redis://localhost:6379/0',
   backend='redis://localhost:6379/0'
)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
   sender.add_periodic_task(60, check_cat.s())
   sender.add_periodic_task(
       crontab(hour=7, minute=30, day_of_week=1),
       check_cat.s()
   )

@app.task
def check_cat():
   if random() < 0.5:
       print("Кот ничего не сломал.")
   else:
       print("Кот что-то сломал...")


# celery -A tasks beat
# celery -A tasks worker -B

from celery import group
from tasks import buy_milk, buy_bread

task1 = buy_milk.s(7)
task2 = buy_bread.s(5)

task_group = group(task1, task2)
result = task_group.apply_async()

results = result.get()
print(results)  # [7, 5]

# _______

from celery import chain
from tasks import fetch_user_name, greeting_user

task1 = fetch_user_name.s(1)
task2 = greeting_user.s()

task_chain = chain(task1 | task2)
result = task_chain.apply_async()

final_result = result.get()
print(final_result)  # Здравствуй, Пётр Первый!


# __---------

from tasks import heavy_task

def get_factorial(arg):
   result = heavy_task.apply_async(args=(arg,))

   while not result.ready():
       # Задача ещё выполняется
       pass

   if result.successful():
       result_value = result.get()
   else:
       # Информация об ошибке
       result_value = result.result

   print(result_value)

get_factorial(50)
# 608281864034267560872252163321295376887552831379210240000000000
get_factorial('Сейчас будет ошибка')
# 'str' object cannot be interpreted as an integer