
def test_cadastrar_usuario(client):
    response = client.post(
        "/users/",
        json={
            "name": "Usuario Teste",
            "email": "teste@devtrack.com",
            "password": "SenhaTeste123"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Usuario Teste"
    assert response.json()["email"] == "teste@devtrack.com"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


def test_impedir_email_duplicado(client):
    dados = {
        "name": "Usuario Teste",
        "email": "duplicado@devtrack.com",
        "password": "SenhaTeste123"
    }

    primeira_resposta = client.post("/users/", json=dados)
    segunda_resposta = client.post("/users/", json=dados)

    assert primeira_resposta.status_code == 201
    assert segunda_resposta.status_code == 409


def test_impedir_email_invalido(client):
    response = client.post(
        "/users/",
        json={
            "name": "Usuario Teste",
            "email": "email-invalido",
            "password": "SenhaTeste123"
        }
    )

    assert response.status_code == 422


from app.models.user import User
from app.core.security import verificar_senha


def test_senha_armazenada_com_hash(db, client):
    dados = {
        "name": "Teste Segurança",
        "email": "seguranca@devtrack.com",
        "password": "SenhaSegura123"
    }

    response = client.post("/users/", json=dados)

    assert response.status_code == 201

    usuario = db.query(User).filter(
        User.email == dados["email"]
    ).first()

    assert usuario is not None
    assert usuario.password_hash != dados["password"]
    assert verificar_senha(
        dados["password"],
        usuario.password_hash
    )
