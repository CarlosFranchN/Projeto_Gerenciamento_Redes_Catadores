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

├── backend
│   ├── alembic
│   │   ├── versions
│   │   │   ├── 66203f355943_cria_tabela_categoriaresiduo_e_linka_em_.py
│   │   │   ├── ccabf74e1aeb_adiciona_tabela_usuarios.py
│   │   │   ├── edeaa421a717_versao_3_0_implementa_arquitetura_.py
│   │   │   └── f8b17a4befaa_ajusta_transacaofinanceira_para_usar_.py
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
│   │   │   ├── categoria.py
│   │   │   ├── compra.py
│   │   │   ├── comprador.py
│   │   │   ├── financeiro.py
│   │   │   ├── material.py
│   │   │   ├── parceiro.py
│   │   │   ├── recebimento.py
│   │   │   ├── relatorio.py
│   │   │   ├── tipo_parceiro.py
│   │   │   ├── usuario.py
│   │   │   └── venda.py
│   │   ├── routers
│   │   │   ├── __init__.py
│   │   │   ├── associacoes.py
│   │   │   ├── auth.py
│   │   │   ├── categoria.py
│   │   │   ├── compradores.py
│   │   │   ├── compras.py
│   │   │   ├── estoque.py
│   │   │   ├── financeiro.py
│   │   │   ├── materiais.py
│   │   │   ├── parceiros.py
│   │   │   ├── recebimentos.py
│   │   │   ├── relatorio.py
│   │   │   ├── tipos_parceiro.py
│   │   │   └── vendas.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├── schema_associacao.py
│   │   │   ├── schema_categoria.py
│   │   │   ├── schema_compra.py
│   │   │   ├── schema_comprador.py
│   │   │   ├── schema_estoque.py
│   │   │   ├── schema_financeiro.py
│   │   │   ├── schema_material.py
│   │   │   ├── schema_parceiro.py
│   │   │   ├── schema_recebimento.py
│   │   │   ├── schema_relatorio.py
│   │   │   ├── schema_tipo_parceiro.py
│   │   │   ├── schema_usuario.py
│   │   │   └── schema_venda.py
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   └── models.py
│   ├── .gitignore
│   ├── alembic.ini
│   ├── criar_usuario.py
│   └── requirements.txt
├── frontend
│   ├── app.html
│   ├── app.js
│   ├── foto1.png
│   ├── foto2.png
│   ├── foto3.png
│   ├── foto4.png
│   ├── foto5.jpg
│   ├── index.html
│   └── logo.png
└── README.md
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


## Instalação e Execução
    🧩 Pré-requisitos

Python 3.11+

PostgreSQL (Banco de dados local rodando)

Git

### 1️⃣ Configuração do Backend (API)
#### 1. Clone o repositório
```
git clone https://github.com/SEU_USUARIO/rede-catadores.git
cd rede-catadores/backend
```
#### 2. Crie e ative o ambiente virtual
```
python -m venv venv
Windows: .\venv\Scripts\activate
Linux/Mac: source venv/bin/activate
```
#### 3. Instale as dependências
```
pip install -r requirements.txt
```
#### 4. Configure as variáveis de ambiente
```
#Crie um arquivo .env na pasta backend/ com o conteúdo:
DATABASE_URL="postgresql+psycopg://USUARIO:SENHA@localhost/rede_catadores_db"
SECRET_KEY="sua_chave_super_secreta"
ALGORITHM="HS256"
```
#### 5. Crie o Banco de Dados
```
#(Certifique-se que o banco 'rede_catadores_db' existe no seu Postgres)
alembic upgrade head
```

#### 6. Crie o usuario 
```
  # no terminal
  python criar_usuario.py
```
#### 7. Inicie o Servidor
```
uvicorn app.main:app --reload
```

#### 8. Executar o Front
```
  cd Projeto_Gerenciamento_Redes_Catadores/frontend
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

## 🛣️ Roadmap (Próximos Passos)

- [x] **V1.0:** CRUDs básicos (Materiais, Associações).
- [x] **V2.0:** Implementação de Vendas e Estoque Dinâmico.
- [x] **V3.0:** Arquitetura de Parceiros Híbridos e Módulo de Compras.
- [x] **V3.1:** Implementação de Autenticação JWT (Backend + Frontend).
- [x] **V3.2:** Implementação do Módulo Financeiro (Livro Caixa) com integração automática de Compras/Vendas.
- [ ] **V3.3:** Implementação de Testes Automatizados (`pytest`) no Backend para garantir a estabilidade.
- [ ] **V4.0:** Deploy em produção (Render para Backend + Vercel/GitHub Pages para Frontend).

📄 Licença

Este projeto está sob a licença MIT.
Sinta-se livre para usar, modificar e distribuir.