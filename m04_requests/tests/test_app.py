import unittest
from m04_requests.app.app_wtform import app  # Импортируем именно нужный Flask-приложение


class TestFlaskApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False  # Отключаем CSRF для тестов
        cls.client = app.test_client()

    def test_register_missing_fields(self):
        response = self.client.post("/register", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_register_invalid_phone(self):
        response = self.client.post("/register", json={"phone": "123"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Телефон должен содержать 10 цифр и только цифры", response.json["error"]["phone"])

    def test_ticket_invalid_number(self):
        response = self.client.post("/ticket",
                                    json={"name": "Иван", "family_name": "Петров", "ticket_number": "012345"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Номер билета должен быть 6-значным", response.json["error"]["ticket_number"])

    def test_register_valid_data(self):
        data = {
            "phone": "1234567890",
            "address": "Улица Пушкина",
            "name": "Иванов И.И.",
            "email": "ivanov@example.com",
            "index": 123456
        }
        response = self.client.post("/register", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Регистрация успешна", response.json["message"])

    def test_register_invalid_email(self):
        data = {
            "phone": "1234567890",
            "address": "Улица Пушкина",
            "name": "Иванов И.И.",
            "email": "неправильныйemail",
            "index": 123456
        }
        response = self.client.post("/register", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Некорректный email", response.json["error"]["email"])

    def test_uptime(self):
        response = self.client.get("/uptime")
        self.assertEqual(response.status_code, 200)
        self.assertIn("uptime", response.json)

    def test_ps(self):
        response = self.client.get("/ps?arg=aux")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<pre>", response.data.decode())


if __name__ == "__main__":
    unittest.main()
