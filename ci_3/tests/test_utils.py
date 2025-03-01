import unittest
from ci_3.app.utils import is_adult

class TestIsAdult(unittest.TestCase):
    def test_adult(self):
        """Проверяем возраст 18+"""
        self.assertTrue(is_adult(18))
        self.assertTrue(is_adult(25))
        self.assertTrue(is_adult(100))

    def test_minor(self):
        """Проверяем несовершеннолетних"""
        self.assertFalse(is_adult(17))
        self.assertFalse(is_adult(0))

    def test_negative_age(self):
        """Негативный тест: отрицательный возраст"""
        with self.assertRaises(ValueError):
            is_adult(-5)

    def test_invalid_type(self):
        """Негативный тест: передаем не число"""
        with self.assertRaises(ValueError):
            is_adult("двадцать")
        with self.assertRaises(ValueError):
            is_adult(None)
        with self.assertRaises(ValueError):
            is_adult([18])

# Запуск тестов
if __name__ == "__main__":
    unittest.main()
#
# python -m unittest discover tests
# python -m unittest discover -v