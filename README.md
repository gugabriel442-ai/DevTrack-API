# DevTrack API

API REST desenvolvida com Python e FastAPI para gerenciamento de projetos e tarefas, com autenticação JWT, controle de acesso por usuário e persistência de dados em MySQL.

O projeto foi desenvolvido com foco em aprendizado e aplicação prática de conceitos de desenvolvimento Backend, arquitetura de APIs, segurança e testes automatizados.

## Tecnologias utilizadas

- **Python 3.14** — Linguagem de programação.
- **FastAPI** — Desenvolvimento da API REST.
- **MySQL** — Banco de dados relacional.
- **SQLAlchemy** — ORM para comunicação com o banco de dados.
- **Pydantic** — Validação e estruturação de dados.
- **JWT** — Autenticação e autorização.
- **Argon2** — Hash e proteção de senhas.
- **Pytest** — Testes automatizados.
- **Git e GitHub** — Controle de versão.

## Funcionalidades

### Usuários e autenticação
- Cadastro de usuários.
- Validação de e-mail.
- Criptografia de senhas utilizando hash Argon2.
- Login com autenticação JWT.
- Proteção de rotas privadas.
- Identificação do usuário autenticado.

### Gerenciamento de projetos
- Cadastro de projetos.
- Consulta e listagem de projetos.
- Edição e exclusão.
- Controle de status: ativo, concluído e arquivado.
- Busca por nome.
- Filtros por status.
- Paginação de resultados.

### Gerenciamento de tarefas
- Cadastro de tarefas vinculadas a projetos.
- Listagem de tarefas.
- Edição e exclusão.
- Controle de status: pendente, em andamento e concluída.
- Definição de prazo.
- Busca por título.
- Filtros por status.
- Paginação de resultados.

### Segurança
- Autenticação baseada em JWT.
- Senhas armazenadas utilizando hash Argon2.
- Controle de acesso aos projetos e tarefas por usuário.
- Proteção contra acesso indevido a dados de outros usuários.

## Estrutura do projeto

devtrack-api/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── projects.py
│   │   │   └── tasks.py
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   └── security.py
│   │
│   ├── database/
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│   │
│   └── __init__.py
│
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_auth.py
│   ├── test_projects.py
│   ├── test_tasks.py
│   └── test_users.py
│
├── .env
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
└── test_connection.py

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/devtrack-api.git
```

### 2. Entrar na pasta

```bash
cd devtrack-api
```

### 3. Criar ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 6. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=devtrack_db

JWT_SECRET_KEY=sua_chave_secreta
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Configure também o banco de dados MySQL antes de executar a aplicação.

**Importante:** não compartilhe seu arquivo `.env` nem envie suas credenciais para o GitHub.

### 7. Executar a API

```bash
uvicorn main:app --reload
```

## Documentação da API

Após iniciar o servidor, acesse a documentação interativa:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

A documentação permite visualizar e testar os endpoints diretamente pelo navegador.

## Testes automatizados

O projeto utiliza Pytest para validar o funcionamento da API.

Para executar os testes:

```bash
python -m pytest -v
```

Atualmente, o projeto possui **28 testes automatizados aprovados**, cobrindo:

- Inicialização da API.
- Cadastro e validação de usuários.
- Proteção de senhas.
- Autenticação JWT.
- Proteção de rotas.
- Operações de projetos e tarefas.
- Controle de acesso entre usuários.
- Paginação, filtros e pesquisas.

Os testes utilizam um banco de dados separado (`devtrack_test_db`), evitando alterações no banco principal de desenvolvimento.

## Objetivo do projeto

O DevTrack API foi desenvolvido como projeto de portfólio para consolidar conhecimentos em Python, desenvolvimento Backend, APIs REST, bancos de dados relacionais, autenticação, segurança e testes automatizados.

O desenvolvimento também tem como objetivo aplicar boas práticas de organização de código e construção de aplicações escaláveis.

## Autor

Desenvolvido como projeto de portfólio durante os estudos de Análise e Desenvolvimento de Sistemas.