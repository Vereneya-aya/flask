import unittest
from ci_3.app.weekday import app

class TestWeekdayApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.base_url = "/week"

    def test_correct_weekday(self):
        response = self.app.get(f"{self.base_url}/Анна")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Привет, Анна", response.json["message"])

    def test_empty_name(self):
        response = self.app.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 404)  # Flask выдаст ошибку, если URL не существует

if __name__ == "__main__":
    unittest.main()