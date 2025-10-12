import pytest

def test_criar_usuario(client):
    payload = {
        "user_name": "Lucas Brum",
        "email": "lucas_brum@email.com",
        "password": "senha123"
    }
    res = client.post("/users", json=payload)
    
    assert res.status_code == 201
    data = res.get_json()
    
    assert data["success"] is True
    assert data["message"] == "Usuário criado com sucesso!"
    
    usuario = data["data"]
    assert usuario["user_name"] == "Lucas Brum"
    assert usuario["email"] == "lucas_brum@email.com"
    assert "id" in usuario
