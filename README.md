# Sistema de Gestão da Rede de Catadores ♻️

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?style=for-the-badge&logo=postgresql)
![Status](https://img.shields.io/badge/Status-Fase%201%20Conclu%C3%ADda-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📖 Sobre o Projeto

Sistema **full-stack** desenvolvido para profissionalizar a gestão da **Rede de Catadores de Resíduos Sólidos do Ceará**.

O sistema substitui planilhas manuais por uma aplicação web que controla:
- 🏢 **Gestão de Associações** (10 associações filiadas)
- 📊 **Produção Mensal** (registro de KG por mês)
- 👥 **Grupos de Catadores** (grupos por município)
- 🗺️ **Municípios Filiados** (20+ municípios)
- 💰 **Operações Financeiras** (compras, vendas, doações)
- 📦 **Controle de Estoque** (entradas e saídas)

---

## ✨ Funcionalidades (Fase 1)

### 🌐 Landing Page Pública

- ✅ **Homepage Institucional** - Apresentação da Rede
- ✅ **Lista de Associações** - 10 associações com detalhes (CNPJ, líder, contato)
- ✅ **Produção Mensal** - Gráfico e tabela com produção de 2024
- ✅ **Grupos e Municípios** - Lista de grupos e municípios filiados
- ✅ **Modal de Detalhes** - Informações completas de cada associação
- ✅ **Formulário de Contato** - Para parcerias e doações
- ✅ **Login** - Acesso à área administrativa

### 🔐 Autenticação

- ✅ JWT (JSON Web Tokens) com access e refresh tokens
- ✅ Hash de senhas com Bcrypt
- ✅ Roles de usuário (admin, operador, visualizador)
- ✅ Logout e revogação de tokens

### 🗄️ Banco de Dados

- ✅ 15+ tabelas relacionadas
- ✅ Migrations com Alembic
- ✅ Audit log para rastreabilidade
- ✅ Cache de endereços (BrasilAPI)



---

## 🛠️ Arquitetura Técnica



O projeto adota uma **Arquitetura Monolítica Modular**, onde o backend é dividido em camadas claras de responsabilidade, facilitando manutenção e escalabilidade.

### Backend (FastAPI + PostgreSQL)

```
.
├── backend/
│   ├── app/                # Código fonte da API
│   ├── alembic/            # Versões do banco de dados
│   ├── scripts/            # Scripts de automação e população
│   ├── Dockerfile          # Receita da imagem do backend
│   ├── docker-compose.yml  # Orquestração (API + Banco)
│   ├── .env                # Variáveis sensíveis (não commitado)
│   └── requirements.txt    # Dependências Python
├── frontend/
│   ├── src/                # Componentes React
│   ├── public/             # Imagens e assets
│   └── package.json        # Dependências Node/React
└── README.md
```
---

## 🚀 Como Rodar o Projeto (Modo Rápido com Docker)
A forma mais fácil de rodar o projeto em qualquer máquina (Windows, Linux ou Mac) é usando o Docker. Você não precisará instalar Python ou PostgreSQL localmente.

### 1️⃣ Pré-requisitos
Docker Desktop instalado.

Git para clonar o projeto.

### 2️⃣ Configuração do Ambiente (.env)
Na pasta backend/, crie um arquivo chamado .env e cole o seguinte conteúdo:

```bash 

# Configurações do Banco de Dados
POSTGRES_USER=postgres
POSTGRES_PASSWORD=4796
POSTGRES_DB=catadores_db

# URL de Conexão (Importante: @db é o nome do serviço no Docker)
DATABASE_URL=postgresql+psycopg://postgres:4796@db:5432/catadores_db

# Segurança e Autenticação
SECRET_KEY=sua_chave_secreta_aqui_32_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

```
### 3️⃣ Subindo os Contêineres
Abra o terminal na pasta raiz do projeto e execute:
```bash
# Entrar na pasta do backend e subir a infra
cd backend
docker compose up -d --build
```

### 4️⃣ Preparando o Banco de Dados (Migrações e Dados)
Com os contêineres rodando, execute os comandos abaixo para criar as tabelas e inserir os dados iniciais:

```bash

# 1. Criar as tabelas (Alembic)
docker exec -it catadores_api alembic upgrade head

# 2. Criar usuário administrador e popular dados
docker exec -it catadores_api python scripts/create_usuario.py
docker exec -it catadores_api python scripts/popular.py

```

### 5️⃣ Acessando o Sistema
Backend API: http://localhost:8000

Documentação Swagger: http://localhost:8000/docs

Frontend (Landing Page): Abra o arquivo frontend/index.html no seu navegador ou use o Live Server do VS Code.


--- 


📊 Estrutura de Tabelas (Simplificada)
O banco de dados conta com 18 tabelas, incluindo:

usuarios: Gestão de acesso e permissões (RBAC).

associacoes: Cadastro detalhado das 10 associações filiadas.

producao_mensal: Registro histórico de KG por material.

grupos e municipios: Mapeamento geográfico da rede.

audit_logs: Rastreabilidade completa de todas as alterações.

📄 Licença

Este projeto está sob a licença MIT.
Sinta-se livre para usar, modificar e distribuir.