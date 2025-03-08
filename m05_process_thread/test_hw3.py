import unittest

from m05_process_thread.hw_3 import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def test_ignore_zero_division(self):
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / 0  # Ошибка игнорируется
        except Exception:
            self.fail("Ошибка не должна была прокинуться")

    def test_raise_unexpected_error(self):
        with self.assertRaises(TypeError):
            with BlockErrors({ZeroDivisionError}):
                a = 1 / "0"  # TypeError должен прокинуться

    def test_nested_blocks(self):
        try:
            with BlockErrors({TypeError}):  # Внешний блок
                with BlockErrors({ZeroDivisionError}):  # Внутренний блок
                    a = 1 / "0"  # TypeError
            # Ошибка должна игнорироваться внешним блоком
        except Exception:
            self.fail("Ошибка не должна была прокинуться")

    def test_ignore_all_exceptions(self):
        try:
            with BlockErrors({Exception}):
                a = 1 / "0"  # TypeError
        except Exception:
            self.fail("Ошибка не должна была прокинуться")

if __name__ == "__main__":
    unittest.main()