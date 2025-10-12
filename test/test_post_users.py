def test_create_user_success(client):
    r = client.post("/users", json={
        "user_name": "Lucas1",
        "email": "lucas1@ex.com",
        "password": "minhaSenhaSegura123"
    })

    assert r.status_code == 201

    body = r.get_json()

    assert body["success"] is True
    assert body["message"] == "User created successfully!"
    assert "data" in body

    data = body["data"]
    assert data["user_name"] == "Lucas1"      
    assert data["email"] == "lucas1@ex.com"
    assert "id" in data               


def test_create_user_missing_fields(client):
    r = client.post("/users", json={
        "user_name": "Lucas2",
        "email": "lucas2@ex.com"
    })

    assert r.status_code == 400
    body = r.get_json()
    assert body["success"] is False
    assert "message" in body


def test_create_user_duplicate_email(client):
    client.post("/users", json={
        "user_name": "Lucas3",
        "email": "lucas3@ex.com",
        "password": "senha123"
    })

    r = client.post("/users", json={
        "user_name": "Lucas3",
        "email": "lucas3@ex.com",  
        "password": "outraSenha"
    })

    assert r.status_code == 400  
    body = r.get_json()
    assert body["success"] is False
    assert "Email already registered." in body["message"]