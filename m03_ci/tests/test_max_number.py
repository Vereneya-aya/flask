import unittest
from m03_ci.app.routes import app

class TestMaxNumberApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.base_url = "/max_number"

    def test_correct_max_number(self):
        response = self.app.get(f"{self.base_url}/1/2/3/10/5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["max_number"], 10)

    def test_incorrect_input(self):
        response = self.app.get(f"{self.base_url}/1/abc/3")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

if __name__ == "__main__":
    unittest.main()

