
3.7 Методы класса TestCase
Четыре метода класса TestCase

На практике можно часто встретить методы setUp, setUpClass, tearDown и tearDownClass. Давайте узнаем, что они делают и для чего они нужны.

В качестве примера для тестирования будем использовать класс Student в файле models.py:

class Student:
    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age


    def set_age(self, value):
        if value <= 0:
            raise ValueError("Возраст должен быть положительным числом")
        self.age = value


setUp
Метод вызывается перед запуском каждого теста и позволяет не писать один и тот же код по созданию экземпляра тестируемого класса. Сравните код с setUp и без него.



Код без использования setUp
В каждом тесте создаём экземпляр студента.

from unittest import TestCase
from models import Student
class StudentTestCase(TestCase):
    def test_default_name_is_none(self):
        student = Student()
        self.assertIsNone(student.name)
    def test_set_invalid_age(self):
        student = Student()
        with self.assertRaises(ValueError):
            student.set_age(-100)


Код с использованием setUp
Перед запуском каждого теста заново создаём экземпляр студента, который можно будет использовать в тестах.

from unittest import TestCase
from models import Student

class StudentTestCase(TestCase):
    def setUp(self):
        self.student = Student()

    def test_default_name_is_none(self):
        self.assertIsNone(self.student.name)

    def test_set_invalid_age(self):
        with self.assertRaises(ValueError):
            self.student.set_age(-100)
Метод assertIsNone проверяет, что значение переменной равно None. Метод assertRaises проверяет, что определённое исключение было вызвано в процессе выполнения программы. Вот перечень наиболее популярных assert-методов:

Метод

Проверяет

assertEqual(a, b)

a == b

assertNotEqual(a, b)

a != b

assertTrue(x)

bool(x) is True

assertFalse(x)

bool(x) is False

assertIs(a, b)

a is b

assertIsNot(a, b)

a is not b

assertIsNone(x)

x is None

assertIsNotNone(x)

x is not None

assertIn(a, b)

a in b

assertNotIn(a, b)

a not in b

assertIsInstance(a, b)

isinstance(a, b)

assertNotIsInstance(a, b)

not isinstance(a, b)

Подробнее об assert-методах читайте в официальной документации.



tearDown
Метод вызывается после запуска каждого теста и позволяет очистить или закрыть ресурсы. Например, удалить созданные в процессе тестирования файлы или закрыть подключение к базе данных.

В связке с setUp можно замерять время работы каждого теста:

import time
from unittest import TestCase
class PerformanceTest(TestCase):
    def setUp(self):
        self.start = time.perf_counter()
    def tearDown(self):
        self.end = time.perf_counter()
        print(self.id(), self.end - self.start)
    def test_million_appends(self):
        N = 1_000_000
        lst = []
        for i in range(N):
            lst.append(i)
        self.assertListEqual(lst, list(range(N)))
time.perf_counter() возвращает текущее время с наибольшим доступным разрешением.

self.id() выдаст название текущего теста в таком формате: __main__.PerformanceTest.test_million_appends



setUpClass
Метод вызывается перед запуском всех тестов в этом классе. Он позволяет задать общие настройки и открыть ресурсы, которые будут использованы всеми тестами.

Здесь, например, мы можем создать тестовый клиент Flask-приложения:

from unittest import TestCase
from hello_word_with_day import app
class TestHelloWorldWithDayApp(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        cls.base_url: str = '/hello-world/'
    def test_can_get_correct_username_with_weekdate(self):
        username: str = 'username'
        response = self.app.get(self.base_url + username)
        response_text: str = response.data.decode()
        self.assertIn(username, response_text)
Заметьте, что это классовый метод, поэтому мы используем декоратор classmethod.



tearDownClass
Метод вызывается после завершения всех тестов в этом классе. Он позволяет закрыть ресурсы, которые были открыты в setUpClass. А также очистить данные, созданные в результате тестирования.

Например, в setUpClass мы можем открыть файл, в который будем складывать результаты тестирования. А в tearDownClass — закрыть его.

import time
from unittest import TestCase
class PerformanceTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file = open("test_log.txt", "a")
    def setUp(self):
        self.start = time.perf_counter()
    def test_million_appends(self):
        N = 1_000_000
        lst = []
        for i in range(N):
            lst.append(i)
        self.assertListEqual(lst, list(range(N)))
    def test_sum_of_numbers(self):
        N = 1_000_000
        self.assertEqual(sum(range(N)), N * (N + 1) // 2)
    def tearDown(self):
        self.end = time.perf_counter()
        print(self.id(), self.end - self.start, file=self.file)
    @classmethod
    def tearDownClass(cls):
        cls.file.close()
В файле увидим следующий результат:

__main__.PerformanceTest.test_million_appends 0.09666280300007202

__main__.PerformanceTest.test_sum_of_numbers 0.011858064999614726



Заключение
Вспомним, для чего нужен каждый из рассмотренных методов:

setUp запускается перед каждым тестом;
tearDown запускается после каждого теста;
setUpClass запускается перед всеми тестами;
tearDownClass запускается после всех тестов.
В setUp и setUpClass мы открываем ресурсы, настраиваем тестируемый объект, создаём необходимые файлы, подключаемся к базе данных. В tearDown и tearDownClass — закрываем ресурсы, удаляем созданные файлы, отключаемся от базы данных.

Помимо четырёх рассмотренных методов, есть и другие. Почитайте о них в документации.




