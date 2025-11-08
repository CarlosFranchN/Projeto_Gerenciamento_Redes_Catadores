# Sistema de Gestão da Rede de Catadores ♻️

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?style=for-the-badge&logo=postgresql)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![Status](https://img.shields.io/badge/Status-MVP%20v3.0-success?style=for-the-badge)

---

## 📖 Sobre o Projeto

Este é um sistema **full-stack** desenvolvido para profissionalizar a gestão da **Rede de Catadores de Resíduos Sólidos**.  
O sistema substitui planilhas manuais por uma aplicação web robusta que controla o fluxo completo de materiais — desde a **entrada (por doação ou compra)** até a **venda para a indústria recicladora**.

A versão atual (**v3.0**) introduziu uma **arquitetura híbrida** capaz de gerenciar diferentes tipos de parceiros e operações financeiras complexas, mantendo um controle de **estoque auditável em tempo real**.

---

## ✨ Funcionalidades Principais (v3.0)

### 🏗️ Gestão de Parceiros & Compradores

- **Base Unificada de Parceiros:** Cadastro centralizado de quem fornece material, classificado por tipo:
  - 🤝 **Associações/Cooperativas:** Com dados detalhados (Líder, CNPJ, Telefone).
  - 🏛️ **Órgãos Públicos:** Prefeituras, Secretarias.
  - 🏭 **Empresas Privadas:** Geradores de resíduos comerciais.
  - 👤 **Catadores Individuais:** Autônomos.
- **Gestão de Compradores:** Cadastro de clientes (indústrias, depósitos) para quem a rede vende o material consolidado.

---

### 🚚 Operações de Entrada (Híbridas)

O sistema diferencia duas formas de entrada de material, ambas alimentando o mesmo estoque físico:

1. **📥 Recebimentos (Doações):** Entradas sem custo financeiro para a Rede (vindas de Associações, Órgãos Públicos, etc.).  
2. **💸 Compras:** Aquisições de material com registro de valor pago (R$), permitindo cálculo de custos.

---

### 📤 Operações de Saída

- **Vendas:** Registro de saída de material para Compradores, com cálculo automático de receita.

---

### 📊 Inteligência & Controle

- **Estoque em Tempo Real:** Calculado dinamicamente (`Entradas + Compras - Vendas`), garantindo integridade sem depender de um campo estático.
- **Relatórios Gerenciais:**
  - Balanço por período.
  - Performance por Material (Kg recebidos vs. vendidos).
  - Ranking de Parceiros (Quem mais doou/vendeu para a rede).
  - **Lucro Bruto:** `Receita Total de Vendas - Custo Total de Compras`.

---

### 🔐 Segurança (Backend Ready)

- Estrutura de autenticação JWT (JSON Web Tokens) implementada no Backend.  
- Hash de senhas com Bcrypt.  
- *(Integração com frontend em andamento).*

---

## 🛠️ Arquitetura Técnica

O projeto adota uma **Arquitetura Monolítica Modular**, onde o backend é dividido em camadas claras de responsabilidade, facilitando manutenção e escalabilidade.

```plaintext
backend/app/
├── core/         # Configurações (env) e Segurança (Auth JWT)
├── models.py     # Definição das Tabelas (SQLAlchemy ORM)
├── schemas/      # Contratos de Dados (Pydantic) - Validação de Entrada/Saída
│   ├── schema_parceiro.py
│   ├── schema_venda.py
│   └── ...
├── crud/         # Regras de Negócio e Acesso ao Banco
│   ├── crud_estoque.py   # Lógica complexa de cálculo de estoque
│   ├── crud_relatorio.py # Agregações para dashboards
│   └── ...
└── routers/      # Endpoints da API (Controllers)
    ├── auth.py
    ├── recebimentos.py
    └── ...


⚙️ Instalação e Execução
🧩 Pré-requisitos

Python 3.11+

PostgreSQL (Banco de dados local rodando)

Git

1️⃣ Configuração do Backend (API)
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/rede-catadores.git
cd rede-catadores/backend

# 2. Crie e ative o ambiente virtual
python -m venv venv
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
# Crie um arquivo .env na pasta backend/ com o conteúdo:
# DATABASE_URL="postgresql+psycopg://USUARIO:SENHA@localhost/rede_catadores_db"
# SECRET_KEY="sua_chave_super_secreta"
# ALGORITHM="HS256"

# 5. Crie o Banco de Dados
# (Certifique-se que o banco 'rede_catadores_db' existe no seu Postgres)
alembic upgrade head

# 6. Inicie o Servidor
uvicorn app.main:app --reload


🔗 A API estará disponível em: http://127.0.0.1:8000

📘 Documentação interativa: http://127.0.0.1:8000/docs

2️⃣ Execução do Frontend (Interface)

O frontend foi construído para ser ultra-leve, sem necessidade de npm ou build complexos para o MVP.
# Abra um novo terminal e navegue para a pasta frontend
cd ../frontend

# Inicie um servidor HTTP simples
python -m http.server 8001


🛣️ Roadmap (Próximos Passos)
[x] V1.0: CRUDs básicos de Materiais e Associações.

[x] V2.0: Implementação de Vendas e Controle de Estoque Dinâmico.

[x] V3.0: Arquitetura de Parceiros Híbridos e Módulo de Compras.

[ ] V3.1: Integração do Login (JWT) no Frontend.

[ ] V3.2: Implementação de Testes Automatizados (pytest) no Backend.

[ ] V4.0: Deploy em produção (Render + GitHub Pages/Vercel).

📄 Licença

Este projeto está sob a licença MIT.
Sinta-se livre para usar, modificar e distribuir.