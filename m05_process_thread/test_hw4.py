import unittest
import io

from m05_process_thread.hw_4 import Redirect


class TestRedirect(unittest.TestCase):
    def test_redirect_stdout(self):
        buffer = io.StringIO()
        with Redirect(stdout=buffer):
            print("Hello stdout test")
        self.assertEqual(buffer.getvalue().strip(), "Hello stdout test")

    def test_redirect_stderr(self):
        buffer = io.StringIO()
        with Redirect(stderr=buffer):
            try:
                raise Exception("Error message")
            except Exception:
                import traceback
                traceback.print_exc()  # Явно отправляем исключение в stderr
        self.assertIn("Error message", buffer.getvalue())  # Проверяем содержимое stderr
        
    def test_no_redirection(self):
        buffer = io.StringIO()
        print("Hello terminal", file=buffer)
        self.assertEqual(buffer.getvalue().strip(), "Hello terminal")


if __name__ == "__main__":
    unittest.main()
