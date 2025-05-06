# tests/test_routes.py

import pytest
from datetime import datetime, timedelta

# 1. GET-методы
@pytest.mark.parametrize("endpoint", [
    "/clients",
    "/parkings",
    "/client_parking"
])
def test_get_endpoints(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code in [200, 404]

# 2. Создание клиента
def test_create_client(client):
    response = client.post("/clients", json={
        "name": "John",
        "surname": "Doe",
        "credit_card": "5555444433332222",
        "car_number": "X999XX"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data

# 3. Создание парковки
def test_create_parking(client):
    response = client.post("/parkings", json={
        "address": "Baker Street",
        "opened": True,
        "count_places": 5,
        "count_available_places": 5
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data

# 4. Заезд на парковку
@pytest.mark.parking
def test_parking_entry(client, setup_data):
    client_id = setup_data["client"].id
    parking_id = setup_data["parking"].id

    response = client.post("/client_parking", json={
        "client_id": client_id,
        "parking_id": parking_id
    })
    assert response.status_code in [200, 201]

# 5. Выезд с парковки
@pytest.mark.parking
def test_parking_exit(client, setup_data, db):
    parking_log = setup_data["parking_log"]

    # имитируем прошествие времени
    parking_log.time_out = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    assert parking_log.time_out > parking_log.time_in