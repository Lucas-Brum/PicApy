def test_create_user(client):
    r = client.post("/users", json={"user": "Lucas", "email": "lucas@ex.com", "password": "hash"})

    assert r.status_code == 201

    body = r.get_json()  # Get JSON response body

    assert body["message"] == "Usuário recebido com sucesso"
    assert body["user"] == "Lucas"
    assert body["email"] == "lucas@ex.com"
    
