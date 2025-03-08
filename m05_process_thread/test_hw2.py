import unittest
from hw_2 import app

class CodeExecutionTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_valid_code_execution(self):
        response = self.client.post('/execute', json={'code': "print('Hello')", 'timeout': 5})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello", response.json['stdout'])

    def test_timeout(self):
        response = self.client.post('/execute', json={'code': "import time; time.sleep(10)", 'timeout': 2})
        self.assertEqual(response.status_code, 408)
        self.assertIn("Execution timed out", response.json['error'])

    def test_invalid_input(self):
        response = self.client.post('/execute', json={'code': "print('Hello')"})  # Без тайм-аута
        self.assertEqual(response.status_code, 400)
        self.assertIn("timeout", response.json['details'])

if __name__ == '__main__':
    unittest.main()