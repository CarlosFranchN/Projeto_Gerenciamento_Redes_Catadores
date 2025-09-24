# Backend - Sistema de Gestão da Rede de Catadores

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?style=for-the-badge&logo=postgresql)

## 📜 Sobre o Projeto

Este repositório contém o código-fonte do backend para o Sistema de Gestão e Análise da Rede de Catadores de Resíduos Sólidos de Fortaleza. O objetivo é criar uma API robusta e escalável para digitalizar e otimizar todo o fluxo de recebimento de materiais, controle de estoque, vendas e geração de relatórios estratégicos.

Este projeto segue uma arquitetura monolítica modular e um padrão de design MVC (Model-Schema-Endpoint) para garantir um código limpo, organizado e de fácil manutenção.

---

## 🚀 Tecnologias Principais

* **Linguagem:** Python 3.11+
* **Framework Web:** FastAPI
* **Banco de Dados:** PostgreSQL
* **ORM (Mapeamento Objeto-Relacional):** SQLAlchemy 2.0
* **Migrações de Banco de Dados:** Alembic
* **Validação de Dados:** Pydantic V2
* **Servidor ASGI:** Uvicorn

---

## ⚙️ Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar o ambiente e rodar o projeto em sua máquina local.

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

### 3. Criando o Ambiente Virtual e Instalando as Dependências
É crucial usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
# No Windows (PowerShell):
.\venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate

# Instale todas as dependências a partir do arquivo requirements.txt
pip install -r requirements.txt
```

### 4. Configurando as Variáveis de Ambiente
As configurações sensíveis, como a conexão com o banco de dados, são gerenciadas por um arquivo `.env`. Crie este arquivo na raiz do projeto.

**Arquivo: `.env`**
```env
# Lembre-se de adicionar o .env ao seu .gitignore!
DATABASE_URL="postgresql+psycopg://SEU_USUARIO:SUA_SENHA@localhost/rede_catadores_db"
```
> **Atenção:** Substitua `SEU_USUARIO` e `SUA_SENHA` pelas suas credenciais do PostgreSQL. `rede_catadores_db` é o nome do banco de dados que você deve criar manualmente no seu PostgreSQL via pgAdmin ou outro cliente.

---

## 🏗️ Configurando o Banco de Dados

Com o ambiente pronto, precisamos criar a estrutura de tabelas no banco de dados. Nós usamos o Alembic para gerenciar as "versões" do nosso banco.

Para aplicar todas as migrações e deixar o banco pronto para uso, rode o seguinte comando na raiz do projeto:
```bash
alembic upgrade head
```
Isso irá criar todas as tabelas definidas em `app/models.py`.

---

## 🗄️ Interagindo com o Banco de Dados

Existem duas formas principais de interagir com o banco de dados durante o desenvolvimento para testes e depuração.

### Método 1: Via Cliente Gráfico (Recomendado para Visualização)

Para visualizar as tabelas, checar os dados que foram inseridos e realizar operações manuais, o ideal é usar um cliente de banco de dados gráfico como o **pgAdmin** (instalado com o PostgreSQL) ou o **DBeaver** (uma alternativa popular).

1.  Abra seu cliente de banco de dados.
2.  Crie uma nova conexão com seu servidor local usando as mesmas credenciais do seu arquivo `.env`:
    * **Host:** `localhost`
    * **Port:** `5432`
    * **Maintenance Database:** `rede_catadores_db`
    * **Username:** `SEU_USUARIO`
    * **Password:** `SUA_SENHA`
3.  Após conectar, navegue até `Databases > rede_catadores_db > Schemas > public > Tables`.
4.  Ali você pode clicar com o botão direito em qualquer tabela para ver sua estrutura (`Properties`) ou seus dados (`View/Edit Data`).

### Método 2: Via Terminal Interativo (Para Testes e Debug de Código)

Para testar a lógica do seu código (`crud.py`, `models.py`) de forma rápida, você pode usar um terminal interativo do Python.

1.  Certifique-se de que seu ambiente virtual (`venv`) está ativado.
2.  (Opcional, mas recomendado) Instale o IPython para uma melhor experiência: `pip install ipython`.
3.  Inicie o terminal interativo: `ipython` (ou `python`).
4.  Dentro do terminal, execute os seguintes comandos para carregar seu ambiente e interagir com o banco:

    ```python
    # Importe os componentes necessários
    from app.database import SessionLocal
    from app.models import Material, Associacao

    # Crie uma sessão com o banco de dados
    db = SessionLocal()

    # Agora você pode usar 'db' para fazer consultas!

    # Exemplo 1: Listar todos os materiais
    todos_os_materiais = db.query(Material).all()
    for material in todos_os_materiais:
        print(f"ID: {material.id}, Nome: {material.nome}")

    # Exemplo 2: Adicionar uma nova associação
    # nova_assoc = Associacao(nome="Associação Central")
    # db.add(nova_assoc)
    # db.commit()
    # print(f"Associação '{nova_assoc.nome}' criada com sucesso!")

    # Lembre-se de fechar a sessão ao terminar
    db.close()
    ```

---

## ▶️ Rodando a Aplicação

Para iniciar o servidor de desenvolvimento, use o Uvicorn.

```bash
uvicorn app.main:app --reload
```
* O servidor estará rodando em `http://127.0.0.1:8000`.
* A documentação interativa da API (Swagger UI) estará disponível em `http://127.0.0.1:8000/docs`.
* A documentação alternativa (ReDoc) estará em `http://12-7.0.0.1:8000/redoc`.

O argumento `--reload` faz com que o servidor reinicie automaticamente toda vez que você salvar uma alteração no código.

---

## 🏛️ Estrutura do Projeto

O projeto é organizado da seguinte forma para garantir a separação de responsabilidades:

```
app/
├── core/         # Configurações globais (leitura do .env)
├── crud.py       # Funções que interagem diretamente com o banco de dados
├── database.py   # Configuração da conexão (engine e session do SQLAlchemy)
├── main.py       # Ponto de entrada principal da aplicação FastAPI
├── models.py     # Definição das tabelas do banco (SQLAlchemy Models)
├── routers/      # Organização dos endpoints da API por recurso (Controllers)
└── schemas.py    # Definição dos "contratos" de dados da API (Pydantic Schemas)
alembic/          # Histórico de migrações do banco de dados
```
---