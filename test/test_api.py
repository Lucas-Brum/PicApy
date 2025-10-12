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
    res = client.post("/users", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    
    assert data["success"] is False
    assert data["message"] == "Email already registered."
    

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

def test_get_all_users(client):
    client.post("/users")

    res = client.get("/users")
    assert res.status_code == 200

    data = res.get_json()
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)

    assert data["message"] == "Operation completed successfully"

def test_get_user_by_id(client):
    client.post("/users/1")

    res = client.get("/users/1")
    assert res.status_code == 200

    data = res.get_json()
    assert data["success"] is True
    assert "data" in data

    assert data["message"] == "Operation completed successfully"


def test_not_fount_get_user_by_id(client):
    client.post("/users/2")

    res = client.get("/users/2")
    assert res.status_code == 404

    data = res.get_json()
    assert data["success"] is False
    assert "data" not in data

    assert data["message"] == "User not found"


def test_update_user(client):
    client.post("/users/1")

    payload = {
        "user_name": "Novo Nome",
        "email": "novoemail@email.com"
        }
    
    res = client.put("/users/1", json=payload)
    assert res.status_code == 200

    data = res.get_json()
    assert data["success"] is True
    assert "data" in data

    assert data["message"] == "User updated successfully"


def test_update_user(client):
    client.post("/users/1")

    
    res = client.delete("/users/1")
    assert res.status_code == 200

    data = res.get_json()
    assert data["success"] is True
    assert data["message"] == "User deleted successfully."

