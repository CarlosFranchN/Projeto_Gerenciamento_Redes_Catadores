# Sistema de Gestão da Rede de Catadores

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?style=for-the-badge&logo=postgresql)

## 📜 Sobre o Projeto

Este repositório contém o código-fonte da aplicação full-stack para o Sistema de Gestão e Análise da Rede de Catadores de Resíduos Sólidos de Fortaleza. O objetivo é criar uma solução completa, com um backend robusto e um frontend reativo, para digitalizar e otimizar todo o fluxo de recebimento de materiais, controle de estoque, vendas e geração de relatórios estratégicos.

O projeto segue uma arquitetura monolítica modular no backend e um padrão de design MVC (Model-Schema-Endpoint) para garantir um código limpo, organizado e de fácil manutenção.

---

## 🚀 Tecnologias Principais

* **Backend:**
    * **Linguagem:** Python 3.11+
    * **Framework Web:** FastAPI
    * **Banco de Dados:** PostgreSQL
    * **ORM:** SQLAlchemy 2.0
    * **Migrações:** Alembic
    * **Validação:** Pydantic V2
* **Frontend:**
    * **Biblioteca:** React 18 (via UMD)
    * **Estilização:** TailwindCSS (via CDN)

---

## ⚙️ Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar o ambiente e rodar o projeto completo em sua máquina local.

### 1. Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas:
* [Python 3.11+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)
* [PostgreSQL](https://www.postgresql.org/download/) (um servidor rodando localmente)

### 2. Clonando o Repositório
```bash
git clone [URL_DO_SEU_REPOSITORIO_AQUI]
cd nome-do-repositorio
```

### 3. Configurando o Backend
Navegue até a pasta do backend para configurar o ambiente Python.
```bash
cd backend

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
# No Windows (PowerShell):
.\venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate

# Instale todas as dependências do backend
pip install -r requirements.txt
```

### 4. Configurando as Variáveis de Ambiente
As configurações sensíveis são gerenciadas por um arquivo `.env` dentro da pasta `backend`.

**Arquivo: `backend/.env`**
```env
# Lembre-se de adicionar o .env ao seu .gitignore!
DATABASE_URL="postgresql+psycopg://SEU_USUARIO:SUA_SENHA@localhost/rede_catadores_db"
```
> **Atenção:** Substitua `SEU_USUARIO` e `SUA_SENHA` pelas suas credenciais do PostgreSQL. `rede_catadores_db` é o nome do banco de dados que você deve criar manualmente no seu PostgreSQL via pgAdmin ou outro cliente.

---

## 🏗️ Configurando o Banco de Dados

Com o ambiente do backend pronto, precisamos criar a estrutura de tabelas no banco de dados.

Dentro da pasta `backend/` (com o `venv` ativado), rode o seguinte comando:
```bash
alembic upgrade head
```
Isso irá criar todas as tabelas definidas em `app/models.py`.

---

## ▶️ Rodando a Aplicação (Backend e Frontend)

Para rodar o sistema completo, você precisará de **dois terminais abertos simultaneamente**.

### **Terminal 1: Rodando o Backend (API)**
Neste terminal, você iniciará o servidor FastAPI.

```bash
# Navegue até a pasta do backend
cd backend

# Ative o ambiente virtual (se ainda não estiver)
.\venv\Scripts\activate

# Inicie o servidor Uvicorn
uvicorn app.main:app --reload --port 8000
```
* O servidor da API estará rodando em `http://127.0.0.1:8000`.
* A documentação interativa (Swagger UI) estará disponível em `http://127.0.0.1:8000/docs`.

### **Terminal 2: Rodando o Frontend (Interface)**
Neste segundo terminal, você servirá o arquivo `index.html`.

```bash
# Navegue até a pasta do frontend
cd frontend

# Inicie um servidor HTTP simples do Python
python -m http.server 8001
```
* A interface do usuário estará acessível em `http://127.0.0.1:8001`.

Abra `http://127.0.0.1:8001` no seu navegador para usar a aplicação.

---

## 🌐 Principais Endpoints da API

A API do backend expõe os seguintes endpoints principais para manipulação dos dados:

* `POST /materiais/` - Cria um novo tipo de material.
* `GET /materiais/` - Lista todos os materiais.
* `POST /associacoes/` - Cadastra uma nova associação.
* `GET /associacoes/` - Lista todas as associações ativas.
* `POST /compradores/` - Cadastra um novo comprador.
* `GET /compradores/` - Lista todos os compradores.
* `POST /entradas/` - Registra uma nova entrada de material.
* `GET /entradas/` - Lista o histórico de entradas.
* `POST /vendas/` - Registra uma nova venda com seus itens.
* `GET /vendas/` - Lista o histórico de vendas.

---

## 🏛️ Estrutura do Projeto

O projeto é dividido em duas pastas principais na raiz: `backend` e `frontend`.

```
projeto_raiz/
├── backend/      # Aplicação FastAPI (API)
│   ├── .env
│   ├── alembic.ini
│   ├── app/
│   │   ├── core/
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   └── schemas.py
│   └── alembic/
└── frontend/     # Aplicação React/HTML (Interface do Usuário)
    └── index.html
```
---