import math
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Tuple, Dict

@dataclass(order=True)
class Task:
    priority: int
    func: Callable = field(compare=False)
    args: Tuple = field(default_factory=tuple, compare=False)
    kwargs: Dict = field(default_factory=dict, compare=False)

    def execute(self) -> None:
        self.func(*self.args, **self.kwargs)

    def __str__(self):
        task_str = self.func.__name__ + '('

        f_args = ', '.join(map(repr, self.args))
        task_str += f_args

        if self.kwargs:
            f_kwargs = ', '.join(
                f'{k}={v!r}' for k, v in self.kwargs.items()
            )
            task_str += ', ' + f_kwargs

        task_str += ')'
        return f'{task_str} [priority={self.priority}]'

class TaskQueue:
    def __init__(self):
        self.queue = deque()

    def add_task(self, task: Task) -> None:
        print('Добавлена задача:', task)
        # Вставляем в очередь по приоритету
        if not self.queue:
            self.queue.append(task)
        else:
            for idx, existing_task in enumerate(self.queue):
                if task.priority > existing_task.priority:
                    self.queue.insert(idx, task)
                    break
            else:
                self.queue.append(task)

    def execute_tasks(self) -> None:
        while self.queue:
            task = self.queue.popleft()
            print('Исполняется задача:', task)
            task.execute()
        print('Все задачи были успешно выполнены')

if __name__ == '__main__':
    queue = TaskQueue()
    queue.add_task(Task(
        priority=1,
        func=time.sleep,
        args=(1,)
    ))
    queue.add_task(Task(
        priority=5,
        func=print,
        args=('Hello', 'World'),
        kwargs={'sep': '_'}
    ))
    queue.add_task(Task(
        priority=10,
        func=math.factorial,
        args=(50,)
    ))
    queue.execute_tasks()