import pytest
from app import app
from model.data_base import DataBase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_db():
    db = DataBase()
    db.create_table() 
    db.cursor.execute("DELETE FROM users")
    db.conn.commit()
    db.close()


def test_create_user(client):
    payload = {
        "user_name": "Lucas",
        "email": "lucas@pipcpay.com",
        "password": "P@ssword1234"
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["message"] == "User created successfully!"
    usuario = data["data"]
    assert usuario["user_name"] == "Lucas"
    assert usuario["email"] == "lucas@pipcpay.com"
    assert "id" in usuario

def test_erro_duplicate_create_user(client):
    payload = {
        "user_name": "Lucas",
        "email": "lucas@pipcpay.com",
        "password": "P@ssword1234"
    }
    client.post("/users", json=payload) 
    res = client.post("/users", json=payload)  
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert data["message"] == "Email already registered."

def test_get_all_users(client):
    payload = {
        "user_name": "Lucas",
        "email": "lucas2@pipcpay.com",
        "password": "P@ssword1234"
    }
    client.post("/users", json=payload) 
    res = client.get("/users")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 1
    assert data["data"][0]["email"] == "lucas2@pipcpay.com"
    assert data["message"] == "Operation completed successfully"

def test_get_user_by_id(client):
    payload = {
        "user_name": "Lucas",
        "email": "lucas3@pipcpay.com",
        "password": "P@ssword1234"
    }
    res_create = client.post("/users", json=payload)
    user_id = res_create.get_json()["data"]["id"]
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["id"] == user_id
    assert data["message"] == "Operation completed successfully"

def test_not_found_get_user_by_id(client):
    res = client.get("/users/999")
    assert res.status_code == 404
    data = res.get_json()
    assert data["success"] is False
    assert "data" not in data
    assert data["message"] == "User not found"

def test_update_user(client):
    payload = {
        "user_name": "Lucas",
        "email": "lucas4@pipcpay.com",
        "password": "P@ssword1234"
    }
    res_create = client.post("/users", json=payload)
    user_id = res_create.get_json()["data"]["id"]

    update_payload = {
        "user_name": "Novo Nome",
        "email": "novoemail@pipcpay.com"
    }
    res = client.put(f"/users/{user_id}", json=update_payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["user_name"] == "Novo Nome"
    assert data["data"]["email"] == "novoemail@pipcpay.com"
    assert data["message"] == "User updated successfully"

def test_delete_user(client):
    payload = {
        "user_name": "Lucas",
        "email": "lucas5@pipcpay.com",
        "password": "P@ssword1234"
    }
    res_create = client.post("/users", json=payload)
    user_id = res_create.get_json()["data"]["id"]

    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["message"] == "User deleted successfully."


    res_get = client.get(f"/users/{user_id}")
    assert res_get.status_code == 404


def test_error_Username_create_user(client):
    payload = {
        "user_name": "Lucas Brum",
        "email": "lucas_brum@pipcpay.com",
        "password": "P@ssword1234"
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert data["message"] == "Username must be alphanumeric and 3-30 characters long"

def test_error_email_create_user(client):
    payload = {
        "user_name": "LucasBrum",
        "email": "lucas_brumpipcpay.com",
        "password": "P@ssword1234"
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert data["message"] == "Invalid email format"

def test_error_password_create_user(client):
    payload = {
        "user_name": "LucasBrum",
        "email": "lucas_brumpipcpay.com",
        "password": "p@ssword1234"
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert data["message"] == "Invalid email format"

