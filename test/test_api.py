import pytest
from app import app
from model.data_base import DataBase
from flask.testing import FlaskClient
from typing import Generator


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_db() -> None:
    db = DataBase()
    db.create_table()
    db.cursor.execute("DELETE FROM users")
    db.conn.commit()
    db.close()


def test_create_user(client: FlaskClient) -> None:
    payload = {
        "user_name": "Lucas",
        "email": "lucas@pipcpay.com",
        "password": "P@ssword1234",
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    usuario = data["data"]
    assert usuario["user_name"] == "Lucas"
    assert usuario["email"] == "lucas@pipcpay.com"
    assert "id" in usuario


def test_erro_duplicate_create_user(client: FlaskClient) -> None:
    payload = {
        "user_name": "Lucas",
        "email": "lucas@pipcpay.com",
        "password": "P@ssword1234",
    }
    client.post("/users", json=payload)
    res = client.post("/users", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "already" in data["message"].lower()


def test_error_missing_fields(client: FlaskClient) -> None:
    payload = {}
    res = client.post("/users", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    # Pydantic lista os erros por campo
    for field in ["user_name", "email", "password"]:
        assert field in data["message"]


def test_error_invalid_email(client: FlaskClient) -> None:
    payload = {
        "user_name": "LucasBrum",
        "email": "lucas_brumpipcpay.com",
        "password": "P@ssword1234",
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "email" in data["message"].lower()


def test_error_username_regex(client: FlaskClient) -> None:
    payload = {
        "user_name": "Lucas Brum",
        "email": "lucas@pipcpay.com",
        "password": "P@ssword1234",
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "username" in data["message"].lower()


def test_error_password_strength(client: FlaskClient) -> None:
    payload = {
        "user_name": "LucasBrum",
        "email": "lucas@pipcpay.com",
        "password": "password123",
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "password" in data["message"].lower()


def test_get_all_users(client: FlaskClient) -> None:
    payload = {
        "user_name": "Lucas",
        "email": "lucas2@pipcpay.com",
        "password": "P@ssword1234",
    }
    client.post("/users", json=payload)
    res = client.get("/users")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 1


def test_get_user_by_id(client: FlaskClient) -> None:
    payload = {
        "user_name": "Lucas",
        "email": "lucas3@pipcpay.com",
        "password": "P@ssword1234",
    }
    res_create = client.post("/users", json=payload)
    user_id = res_create.get_json()["data"]["id"]
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["id"] == user_id


def test_update_user(client: FlaskClient) -> None:
    payload = {
        "user_name": "Lucas",
        "email": "lucas4@pipcpay.com",
        "password": "P@ssword1234",
    }
    res_create = client.post("/users", json=payload)
    user_id = res_create.get_json()["data"]["id"]

    update_payload = {"user_name": "Novo Nome", "email": "novoemail@pipcpay.com"}
    res = client.put(f"/users/{user_id}", json=update_payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["user_name"] == "Novo Nome"
    assert data["data"]["email"] == "novoemail@pipcpay.com"


def test_delete_user(client: FlaskClient) -> None:
    payload = {
        "user_name": "Lucas",
        "email": "lucas5@pipcpay.com",
        "password": "P@ssword1234",
    }
    res_create = client.post("/users", json=payload)
    user_id = res_create.get_json()["data"]["id"]

    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200

    res_get = client.get(f"/users/{user_id}")
    assert res_get.status_code == 404
