
def criar_usuario_teste(client):
    client.post(
        "/users/",
        json={
            "name": "Usuario Auth",
            "email": "auth@devtrack.com",
            "password": "SenhaTeste123"
        }
    )


def test_login_com_credenciais_corretas(client):
    criar_usuario_teste(client)

    response = client.post(
        "/auth/login",
        data={
            "username": "auth@devtrack.com",
            "password": "SenhaTeste123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_com_senha_incorreta(client):
    criar_usuario_teste(client)

    response = client.post(
        "/auth/login",
        data={
            "username": "auth@devtrack.com",
            "password": "SenhaErrada123"
        }
    )

    assert response.status_code == 401


def test_acesso_com_token_valido(client):
    criar_usuario_teste(client)

    login = client.post(
        "/auth/login",
        data={
            "username": "auth@devtrack.com",
            "password": "SenhaTeste123"
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "auth@devtrack.com"


def test_bloquear_acesso_sem_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_bloquear_acesso_com_token_invalido(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer token_invalido"}
    )

    assert response.status_code == 401
