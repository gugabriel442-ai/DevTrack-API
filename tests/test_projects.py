
def criar_usuario_e_obter_token(client):
    client.post(
        "/users/",
        json={
            "name": "Usuario Projetos",
            "email": "projetos@devtrack.com",
            "password": "SenhaTeste123"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "projetos@devtrack.com",
            "password": "SenhaTeste123"
        }
    )

    return login.json()["access_token"]


def test_criar_projeto(client):
    token = criar_usuario_e_obter_token(client)

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Projeto de Teste",
            "description": "Projeto criado pelo Pytest"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Projeto de Teste"


def test_listar_projetos(client):
    token = criar_usuario_e_obter_token(client)

    client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Projeto Lista",
            "description": "Teste de listagem"
        }
    )

    response = client.get(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_bloquear_projetos_sem_token(client):
    response = client.get("/projects/")

    assert response.status_code == 401

    
def test_editar_projeto(client):
    token = criar_usuario_e_obter_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    projeto = client.post(
        "/projects/",
        headers=headers,
        json={
            "name": "Projeto Original",
            "description": "Descrição original"
        }
    )

    project_id = projeto.json()["id"]

    response = client.put(
        f"/projects/{project_id}",
        headers=headers,
        json={
            "name": "Projeto Atualizado",
            "status": "completed"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Projeto Atualizado"
    assert response.json()["status"] == "completed"


def test_excluir_projeto(client):
    token = criar_usuario_e_obter_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    projeto = client.post(
        "/projects/",
        headers=headers,
        json={
            "name": "Projeto para Excluir",
            "description": "Teste de exclusão"
        }
    )

    project_id = projeto.json()["id"]

    response = client.delete(
        f"/projects/{project_id}",
        headers=headers
    )

    assert response.status_code == 204

    consulta = client.get(
        "/projects/",
        headers=headers
    )

    assert all(
        item["id"] != project_id
        for item in consulta.json()
    )


def test_impedir_acesso_a_projeto_de_outro_usuario(client):
    token_usuario_1 = criar_usuario_e_obter_token(client)

    projeto = client.post(
        "/projects/",
        headers={
            "Authorization": f"Bearer {token_usuario_1}"
        },
        json={
            "name": "Projeto Privado",
            "description": "Projeto do primeiro usuário"
        }
    )

    project_id = projeto.json()["id"]

    client.post(
        "/users/",
        json={
            "name": "Segundo Usuario",
            "email": "segundo@devtrack.com",
            "password": "SenhaTeste123"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "segundo@devtrack.com",
            "password": "SenhaTeste123"
        }
    )

    token_usuario_2 = login.json()["access_token"]

    response = client.put(
        f"/projects/{project_id}",
        headers={
            "Authorization": f"Bearer {token_usuario_2}"
        },
        json={"name": "Tentativa de invasão"}
    )

    assert response.status_code == 404


def test_filtrar_projetos_por_status(client):
    token = criar_usuario_e_obter_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/projects/",
        headers=headers,
        json={"name": "Projeto Ativo"}
    )

    projeto = client.post(
        "/projects/",
        headers=headers,
        json={"name": "Projeto Concluido"}
    )

    project_id = projeto.json()["id"]

    client.put(
        f"/projects/{project_id}",
        headers=headers,
        json={"status": "completed"}
    )

    response = client.get(
        "/projects/?status=completed",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "completed"


def test_buscar_projeto_por_nome(client):
    token = criar_usuario_e_obter_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/projects/",
        headers=headers,
        json={"name": "DevTrack API"}
    )

    response = client.get(
        "/projects/?search=DevTrack",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "DevTrack API"


def test_paginar_projetos(client):
    token = criar_usuario_e_obter_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    for numero in range(3):
        client.post(
            "/projects/",
            headers=headers,
            json={"name": f"Projeto {numero + 1}"}
        )

    response = client.get(
        "/projects/?skip=0&limit=2",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 2

