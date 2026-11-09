
import pytest


@pytest.fixture
def projeto_teste(client):
    # Cadastrar usuário
    usuario = client.post(
        "/users/",
        json={
            "name": "Usuario Tarefas",
            "email": "tarefas@devtrack.com",
            "password": "SenhaTeste123"
        }
    )
    assert usuario.status_code == 201

    # Realizar login
    login = client.post(
        "/auth/login",
        data={
            "username": "tarefas@devtrack.com",
            "password": "SenhaTeste123"
        }
    )
    assert login.status_code == 200

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Criar projeto
    projeto = client.post(
        "/projects/",
        headers=headers,
        json={
            "name": "Projeto de Tarefas",
            "description": "Testes automatizados"
        }
    )
    assert projeto.status_code == 201

    return projeto.json()["id"], headers


def test_criar_tarefa(client, projeto_teste):
    project_id, headers = projeto_teste

    response = client.post(
        f"/projects/{project_id}/tasks/",
        headers=headers,
        json={
            "title": "Criar testes",
            "description": "Testar a API"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Criar testes"
    assert response.json()["status"] == "pending"


def test_listar_tarefas(client, projeto_teste):
    project_id, headers = projeto_teste

    client.post(
        f"/projects/{project_id}/tasks/",
        headers=headers,
        json={"title": "Primeira tarefa"}
    )

    response = client.get(
        f"/projects/{project_id}/tasks/",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_editar_tarefa(client, projeto_teste):
    project_id, headers = projeto_teste

    tarefa = client.post(
        f"/projects/{project_id}/tasks/",
        headers=headers,
        json={"title": "Tarefa original"}
    )

    task_id = tarefa.json()["id"]

    response = client.put(
        f"/projects/{project_id}/tasks/{task_id}",
        headers=headers,
        json={
            "title": "Tarefa atualizada",
            "status": "completed"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa atualizada"
    assert response.json()["status"] == "completed"


def test_excluir_tarefa(client, projeto_teste):
    project_id, headers = projeto_teste

    tarefa = client.post(
        f"/projects/{project_id}/tasks/",
        headers=headers,
        json={"title": "Tarefa para excluir"}
    )

    task_id = tarefa.json()["id"]

    response = client.delete(
        f"/projects/{project_id}/tasks/{task_id}",
        headers=headers
    )

    assert response.status_code == 204

    consulta = client.get(
        f"/projects/{project_id}/tasks/",
        headers=headers
    )

    assert all(
        item["id"] != task_id
        for item in consulta.json()
    )


def test_bloquear_tarefas_sem_token(client):
    response = client.get("/projects/1/tasks/")

    assert response.status_code == 401

def test_impedir_acesso_a_tarefa_de_outro_usuario(client, projeto_teste):
    # Criar primeiro usuário e projeto
    project_id, headers_usuario_1 = projeto_teste

    tarefa = client.post(
        f"/projects/{project_id}/tasks/",
        headers=headers_usuario_1,
        json={"title": "Tarefa privada"}
    )

    task_id = tarefa.json()["id"]

    # Criar segundo usuário
    client.post(
        "/users/",
        json={
            "name": "Segundo Usuario",
            "email": "segundo_tarefas@devtrack.com",
            "password": "SenhaTeste123"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "segundo_tarefas@devtrack.com",
            "password": "SenhaTeste123"
        }
    )

    token_usuario_2 = login.json()["access_token"]

    headers_usuario_2 = {
        "Authorization": f"Bearer {token_usuario_2}"
    }

    # Tentar modificar a tarefa do primeiro usuário
    response = client.put(
        f"/projects/{project_id}/tasks/{task_id}",
        headers=headers_usuario_2,
        json={"title": "Tentativa de alteração"}
    )

    assert response.status_code == 404

    # Tentar excluir a tarefa
    response = client.delete(
        f"/projects/{project_id}/tasks/{task_id}",
        headers=headers_usuario_2
    )

    assert response.status_code == 404


def test_filtrar_tarefas_por_status(client, projeto_teste):
    project_id, headers = projeto_teste

    client.post(
        f"/projects/{project_id}/tasks/",
        headers=headers,
        json={"title": "Tarefa pendente"}
    )

    tarefa = client.post(
        f"/projects/{project_id}/tasks/",
        headers=headers,
        json={"title": "Tarefa concluida"}
    )

    task_id = tarefa.json()["id"]

    client.put(
        f"/projects/{project_id}/tasks/{task_id}",
        headers=headers,
        json={"status": "completed"}
    )

    response = client.get(
        f"/projects/{project_id}/tasks/?status=completed",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "completed"


def test_buscar_tarefa_por_titulo(client, projeto_teste):
    project_id, headers = projeto_teste

    client.post(
        f"/projects/{project_id}/tasks/",
        headers=headers,
        json={"title": "Desenvolver API Python"}
    )

    response = client.get(
        f"/projects/{project_id}/tasks/?search=Python",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Desenvolver API Python"


def test_paginar_tarefas(client, projeto_teste):
    project_id, headers = projeto_teste

    for numero in range(3):
        client.post(
            f"/projects/{project_id}/tasks/",
            headers=headers,
            json={"title": f"Tarefa {numero + 1}"}
        )

    response = client.get(
        f"/projects/{project_id}/tasks/?skip=0&limit=2",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 2
