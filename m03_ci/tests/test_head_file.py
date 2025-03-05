import unittest
import os
from m03_ci.app.head_file import read_file

class TestHeadFile(unittest.TestCase):
    def setUp(self):
        self.test_file = "test.txt"
        with open(self.test_file, "w") as f:
            f.write("Hello, world!")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_file_exists(self):
        result = read_file(self.test_file)
        self.assertEqual(result["content"], "Hello, world!")

    def test_file_not_exists(self):
        result = read_file("missing.txt")
        self.assertEqual(result[1], 404)

    def test_empty_file(self):
        open(self.test_file, "w").close()  # создаем пустой файл
        result = read_file(self.test_file)
        self.assertEqual(result[1], 400)

if __name__ == "__main__":
    unittest.main()

# python -m unittest discover tests