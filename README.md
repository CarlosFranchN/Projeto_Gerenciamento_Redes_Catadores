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

### 📊 Gestão

- ✅ CRUD de Associações
- ✅ CRUD de Produção Mensal
- ✅ CRUD de Grupos
- ✅ CRUD de Municípios
- ✅ CRUD de Usuários
- ✅ CRUD de Materiais e Categorias
- ✅ CRUD de Parceiros e Compradores
- ✅ Registro de Compras, Vendas e Doações

---

## 🛠️ Arquitetura Técnica



O projeto adota uma **Arquitetura Monolítica Modular**, onde o backend é dividido em camadas claras de responsabilidade, facilitando manutenção e escalabilidade.

### Backend (FastAPI + PostgreSQL)

```
├── backend
│   ├── alembic
│   │   ├── versions
│   │   │   ├── 950576b57d5b_add_role_and_created_at_to_usuarios.py
│   │   │   ├── b1a6f58fce3c_create_grupo_and_municipio_tables.py
│   │   │   └── d66031aa8eb1_create_producao_mensal_table.py
│   │   ├── README
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── crud
│   │   │   ├── __init__.py
│   │   │   ├── associacao.py
│   │   │   ├── audit.py
│   │   │   ├── categoria.py
│   │   │   ├── compra.py
│   │   │   ├── comprador.py
│   │   │   ├── endereco.py
│   │   │   ├── financeiro.py
│   │   │   ├── grupo.py
│   │   │   ├── material.py
│   │   │   ├── municipio.py
│   │   │   ├── parceiro.py
│   │   │   ├── producao.py
│   │   │   ├── recebimento.py
│   │   │   ├── relatorio.py
│   │   │   ├── tipo_parceiro.py
│   │   │   ├── token.py
│   │   │   ├── usuario.py
│   │   │   └── venda.py
│   │   ├── routers
│   │   │   ├── __init__.py
│   │   │   ├── associacoes.py
│   │   │   ├── audit.py
│   │   │   ├── auth.py
│   │   │   ├── categoria.py
│   │   │   ├── compradores.py
│   │   │   ├── compras.py
│   │   │   ├── estoque.py
│   │   │   ├── financeiro.py
│   │   │   ├── grupos.py
│   │   │   ├── materiais.py
│   │   │   ├── municipios.py
│   │   │   ├── parceiros.py
│   │   │   ├── producao.py
│   │   │   ├── recebimentos.py
│   │   │   ├── relatorio.py
│   │   │   ├── tipos_parceiro.py
│   │   │   ├── usuarios.py
│   │   │   └── vendas.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├── schema_associacao.py
│   │   │   ├── schema_audit.py
│   │   │   ├── schema_categoria.py
│   │   │   ├── schema_compra.py
│   │   │   ├── schema_comprador.py
│   │   │   ├── schema_endereco.py
│   │   │   ├── schema_estoque.py
│   │   │   ├── schema_financeiro.py
│   │   │   ├── schema_grupo.py
│   │   │   ├── schema_material.py
│   │   │   ├── schema_municipio.py
│   │   │   ├── schema_parceiro.py
│   │   │   ├── schema_producao.py
│   │   │   ├── schema_recebimento.py
│   │   │   ├── schema_relatorio.py
│   │   │   ├── schema_tipo_parceiro.py
│   │   │   ├── schema_token.py
│   │   │   ├── schema_usuario.py
│   │   │   └── schema_venda.py
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   └── models.py
│   ├── .gitignore
│   ├── alembic.ini
│   ├── alembic.ini.backup
│   ├── popular_associacoes.py
│   ├── popular_dados.py
│   ├── popular_producao.py
│   └── requirements.txt
├── frontend
│   ├── src
│   │   ├── data
│   │   │   ├── associacoes.js
│   │   │   ├── grupos.js
│   │   │   ├── index.js
│   │   │   ├── municipios.js
│   │   │   └── producao.js
│   │   ├── scripts
│   │   │   └── render.js
│   │   ├── services
│   │   │   └── api.js
│   │   ├── utils
│   │   │   ├── formatters.js
│   │   │   ├── index.js
│   │   │   ├── loading.js
│   │   │   ├── sanitizers.js
│   │   │   ├── toast.js
│   │   │   └── validators.js
│   │   └── landingPage_app.js
│   ├── app.html
│   ├── app.js
│   ├── foto1.png
│   ├── foto2.png
│   ├── foto4.png
│   ├── foto5.jpg
│   ├── index_old.html
│   └── logo.png
├── README.md
├── foto1.png
├── foto2.png
├── foto4.png
├── foto5.jpg
├── index.html
└── logo.png
```
---


## Programas Necessários (Ambiente)
🚀 Começando
Para rodar este projeto, você precisará ter os seguintes programas instalados na sua máquina:

Python (Versão 3.11 ou superior):

Necessário para rodar o backend (FastAPI) e o servidor simples do frontend.

PostgreSQL (Versão 16+ recomendada):

O banco de dados onde todas as informações são armazenadas.

Git:

Para clonar o repositório.

(Opcional) Cliente de Banco de Dados:

Um software como pgAdmin ou DBeaver para visualizar os dados do PostgreSQL.


### Pré-requisitos

| Programa | Versão | Link |
|----------|--------|------|
| Python | 3.11+ | [python.org](https://python.org) |
| PostgreSQL | 16+ | [postgresql.org](https://postgresql.org) |
| Git | Qualquer | [git-scm.com](https://git-scm.com) |

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/SEU_USUARIO/rede-catadores.git
cd rede-catadores
```

#### 2. Crie e ative o ambiente virtual
```
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
.\venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate


```

#### 3. Instale as dependências
```
pip install -r requirements.txt
```
#### 4. Configure as variáveis de ambiente
```
#Crie um arquivo .env na pasta backend/ com o conteúdo:
DATABASE_URL="postgresql://usuario:senha@localhost:5432/rede_catadores_db"
SECRET_KEY="sua-chave-secreta-muito-forte-32-caracteres"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### 5. Crie o Banco de Dados
```
#(Certifique-se que o banco 'rede_catadores_db' existe no seu Postgres)
alembic upgrade head
```

#### 6. Popular Dados
```
# Criar usuário admin
python criar_usuario.py

# Popular associações
python popular_associacoes_completas.py

# Popular produção
python popular_producao_rede.py

# Popular grupos e municípios
python popular_grupos_municipios.py
```
#### 7. Inicie o Servidor
```
  # Terminal 1 - Backend
  cd backend
  uvicorn app.main:app --reload

  # Terminal 2 - Frontend
  cd frontend
  python -m http.server 8001
```
--- 

``` 
🔗 A API estará disponível em: http://127.0.0.1:8000

📘 Documentação interativa: http://127.0.0.1:8000/docs

2️⃣ Execução do Frontend (Interface)

O frontend foi construído para ser ultra-leve, sem necessidade de npm ou build complexos para o MVP.
# Abra um novo terminal e navegue para a pasta frontend
cd ../frontend

# Inicie um servidor HTTP simples
python -m http.server 8001
``` 

## 📊 Estrutura do Banco de Dados

### Tabelas Principais

| # | Tabela | Descrição | Colunas Principais |
|---|--------|-----------|-------------------|
| 1 | `usuarios` | Usuários do sistema | id, username, hashed_password, role, ativo, created_at |
| 2 | `associacoes` | Associações de catadores | id, parceiro_id, lider, telefone, cnpj, bairro, cidade, uf, status |
| 3 | `parceiros` | Base unificada de parceiros | id, nome, id_tipo_parceiro |
| 4 | `tipo_parceiro` | Tipos de parceiros | id, nome (ASSOCIACAO, ORGAO_PUBLICO, etc.) |
| 5 | `producao_mensal` | Produção mensal por associação | id, associacao_id, mes, ano, kg, valor_venda |
| 6 | `grupos` | Grupos de catadores | id, nome, integrantes, associacao_id, cidade, uf |
| 7 | `municipios` | Municípios filiados | id, nome, uf, qtd_grupos, qtd_associacoes |
| 8 | `materiais` | Materiais recicláveis | id, codigo, nome, id_categoria, unidade_medida |
| 9 | `categoria_residuo` | Categorias de resíduos | id, nome (Plástico, Papel, Metal, etc.) |
| 10 | `compradores` | Clientes que compram da rede | id, nome, cnpj, telefone, email |
| 11 | `compras` | Compras de material | id, codigo_compra, quantidade, valor_pago_total, id_parceiro, id_material |
| 12 | `vendas` | Vendas para indústria | id, codigo, data_venda, id_comprador |
| 13 | `itens_venda` | Itens de cada venda | id, id_venda, id_material, quantidade_vendida, valor_unitario |
| 14 | `recebimentos_doacao` | Doações recebidas | id, codigo_lote, quantidade, id_parceiro, id_material |
| 15 | `transacoes_financeiras` | Registro financeiro | id, tipo, valor, descricao, id_compra_associada, id_venda_associada |
| 16 | `refresh_tokens` | Tokens de sessão | id, usuario_id, token, expires_at, revoked |
| 17 | `audit_logs` | Logs de auditoria | id, usuario_id, acao, tabela_afetada, dados_antigos, dados_novos |
| 18 | `enderecos_cache` | Cache de CNPJs | id, cnpj, logradouro, numero, bairro, cidade, uf |


## 💾 Scripts de População Inicial (Seed Data)

Para que o sistema funcione corretamente logo após a instalação, é necessário popular as tabelas de domínio (tipos, categorias) e os cadastros iniciais. 

Você pode executar os scripts SQL abaixo diretamente no seu cliente de banco de dados (pgAdmin, DBeaver) ou garantir que eles estejam nas migrações do Alembic.

### 1. Tipos de Parceiro e Categorias de Resíduo
Estes dados são fundamentais para o funcionamento dos dropdowns e cadastros.

```sql
-- Inserir Tipos de Parceiro
INSERT INTO tipo_parceiro (id, nome) VALUES
(1, 'ASSOCIACAO'),
(2, 'ORGAO_PUBLICO'),
(3, 'EMPRESA_PRIVADA'),
(4, 'CATADOR_INDIVIDUAL'),
(5, 'OUTRO')
ON CONFLICT (id) DO NOTHING;

-- Inserir Categorias de Resíduo
INSERT INTO categoria_residuo (id, nome) VALUES
(1, 'Plástico'),
(2, 'Papel'),
(3, 'Metal'),
(4, 'Vidro'),
(5, 'Orgânico'),
(6, 'Rejeito'),
(7, 'Eletrônico'),
(8, 'Tetra Pak')
ON CONFLICT (id) DO NOTHING;

-- 1. Inserir os nomes na tabela PARCEIROS (Pai)
INSERT INTO parceiros (nome, id_tipo_parceiro) VALUES
('REDE DE CATADORES', 1),
('ACORES', 1),
('ARAN', 1),
('ASCAJAN', 1),
('MOURA BRASIL', 1),
('MARAVILHA', 1),
('RAIO DE SOL', 1),
('ROSA VIRGÍNIA', 1),
('SOCRELP', 1),
('VIVA A VIDA', 1)
ON CONFLICT (nome) DO NOTHING;

-- 2. Inserir os detalhes na tabela ASSOCIACOES (Filha)
-- Utiliza SELECT para garantir o vínculo correto com o ID gerado acima
INSERT INTO associacoes (parceiro_id, lider, telefone, cnpj, ativo)
SELECT id, 'Leina Mara Rodrigues da Silva Duarte', '(85) 98562-4020', '09.000.185/0001-09', TRUE FROM parceiros WHERE nome = 'REDE DE CATADORES'
UNION ALL
SELECT id, 'LIDIANA SOUSA', '(85) 99436-4061', '04.989.221/0001-95', TRUE FROM parceiros WHERE nome = 'ACORES'
UNION ALL
SELECT id, 'MARIA DA CONCEIÇÃO', '(85) 98575-2728', '07.475.187/0001-29', TRUE FROM parceiros WHERE nome = 'ARAN'
UNION ALL
SELECT id, 'SEBASTIANA DO CARMO', '(85) 98520-7116', '08.612.882/0001-58', TRUE FROM parceiros WHERE nome = 'ASCAJAN'
UNION ALL
SELECT id, 'FRANCSICA RAQUEL', '(85) 99838-2731', '24.293.438/0001-73', TRUE FROM parceiros WHERE nome = 'MOURA BRASIL'
UNION ALL
SELECT id, 'KELSON ALVES', '(85) 99769-9760', '11.058.865/0001-25', TRUE FROM parceiros WHERE nome = 'MARAVILHA'
UNION ALL
SELECT id, 'LEIDIVANIA MARIA', '(85) 99234-0148', '23.668.402/0001-64', TRUE FROM parceiros WHERE nome = 'RAIO DE SOL'
UNION ALL
SELECT id, 'MUSAMARA PEREIRA', '(85) 98962-1862', '09.635.604/0001-89', TRUE FROM parceiros WHERE nome = 'ROSA VIRGÍNIA'
UNION ALL
SELECT id, 'JANETE CABRAL', '(85) 98613-0768', '00.118.784/0001-57', TRUE FROM parceiros WHERE nome = 'SOCRELP'
UNION ALL
SELECT id, 'LAUDIRENE', '(85) 98528-9578', '07.865.301/0001-27', TRUE FROM parceiros WHERE nome = 'VIVA A VIDA';

``` 

## 🛣️ Roadmap
### ✅ Fase 1 - Fundação (Concluída)
Landing page pública funcional
API com CRUDs completos
Banco de dados com migrations
Autenticação JWT
Scripts de população de dados
Frontend modular e reutilizável
### ⏳ Fase 2 - Dashboard Admin (Próxima)
Tela de login funcional
Dashboard com gráficos e KPIs
CRUD de associações (admin)
CRUD de produção mensal
CRUD de grupos e municípios
Logout e gestão de sessão
### ⏳ Fase 3 - Infra e Deploy
Variáveis de ambiente em produção
Backup automático do banco
Deploy frontend (Vercel/Netlify)
Deploy backend (Render/Railway)
HTTPS/SSL
Domínio próprio
Monitoramento (Sentry)

📄 Licença

Este projeto está sob a licença MIT.
Sinta-se livre para usar, modificar e distribuir.