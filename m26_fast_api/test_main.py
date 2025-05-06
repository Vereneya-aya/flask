from fastapi.testclient import TestClient
from main import app
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

client = TestClient(app)

def test_create_and_get_recipe():
    # Создание рецепта
    response = client.post("/recipes", json={
        "title": "Пельмени",
        "description": "Варёные пельмени с мясом",
        "ingredients": "мука, мясо, вода, соль",
        "cooking_time": 30
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Пельмени"

    # Получение списка рецептов
    response = client.get("/recipes")
    assert response.status_code == 200
    assert any(r["title"] == "Пельмени" for r in response.json())

    # Получение по id
    recipe_id = data["id"]
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Пельмени"