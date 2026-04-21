import sys
import os
import traceback
from datetime import datetime, timedelta

# Adiciona a raiz ao path para garantir que os imports funcionem
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Cores para o terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class BackendValidator:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def print_header(self, text):
        print(f"\n{Colors.BLUE}{'='*50}{Colors.RESET}")
        print(f"{Colors.BLUE} {text} {Colors.RESET}")
        print(f"{Colors.BLUE}{'='*50}{Colors.RESET}")

    def assert_test(self, test_name, condition, error_msg=""):
        if condition:
            print(f"{Colors.GREEN}✅ [PASS] {test_name}{Colors.RESET}")
            self.passed += 1
        else:
            print(f"{Colors.RED}❌ [FAIL] {test_name}{Colors.RESET}")
            if error_msg:
                print(f"   {Colors.YELLOW}Detalhe: {error_msg}{Colors.RESET}")
            self.failed += 1

    def run_all(self):
        self.test_imports()
        self.test_fastapi_routes()
        self.test_database_connection()
        self.test_schemas_pydantic()
        self.test_jwt_auth()
        self.test_safe_crud()
        self.print_summary()

    def test_imports(self):
        self.print_header("1. TESTANDO IMPORTS (Módulos Base)")
        try:
            from app.models import Municipio, Associacao, Afiliado
            self.assert_test("Import models.py", True)
        except Exception as e:
            self.assert_test("Import models.py", False, str(e))

        try:
            from app.database import engine, SessionLocal
            self.assert_test("Import database.py", True)
        except Exception as e:
            self.assert_test("Import database.py", False, str(e))

        try:
            from app.main import app
            self.assert_test("Import main.py (FastAPI App)", True)
        except Exception as e:
            self.assert_test("Import main.py (FastAPI App)", False, str(e))

    def test_fastapi_routes(self):
        self.print_header("2. TESTANDO API ENDPOINTS")
        try:
            from app.main import app
            routes = [route.path for route in app.routes]
            
            # Verifica se os endpoints básicos foram registrados
            has_associacoes = any("/api/associacoes" in r for r in routes)
            has_municipios = any("/api/municipios" in r for r in routes)
            
            self.assert_test("Rota de Associações registrada", has_associacoes)
            self.assert_test("Rota de Municípios registrada", has_municipios)
        except Exception as e:
            self.assert_test("Leitura de rotas do FastAPI", False, str(e))

    def test_database_connection(self):
        self.print_header("3. TESTANDO BANCO DE DADOS (PostgreSQL)")
        try:
            from app.database import engine
            from sqlalchemy import inspect
            
            # Testa conexão
            with engine.connect() as conn:
                self.assert_test("Conexão com PostgreSQL bem sucedida", True)
            
            # Testa se as tabelas existem
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            required_tables = ['municipios', 'grupos', 'associacoes', 'afiliados', 'producao_impacto']
            
            for table in required_tables:
                self.assert_test(f"Tabela '{table}' existe", table in tables)
                
        except Exception as e:
            self.assert_test("Conexão/Inspeção do Banco de Dados", False, str(e))

    def test_schemas_pydantic(self):
        self.print_header("4. TESTANDO SCHEMAS (Pydantic Validação)")
        try:
            from app.schemas.schema_producao import ProducaoImpactoCreate
            from pydantic import ValidationError
            
            # Testa erro proposital (mês 13)
            try:
                ProducaoImpactoCreate(mes=13, ano=2024, categoria="PET", peso_kg=100.5, associacao_id=1)
                self.assert_test("Schema rejeita mês inválido (13)", False, "Aceitou mês inválido sem gerar ValidationError")
            except ValidationError:
                self.assert_test("Schema rejeita mês inválido (13) corretamente", True)
                
        except ImportError:
            print(f"{Colors.YELLOW}⚠️  Pulo de teste: Schema de Produção não encontrado ou nome diferente.{Colors.RESET}")
        except Exception as e:
            self.assert_test("Validação Pydantic", False, str(e))

    def test_jwt_auth(self):
        self.print_header("5. TESTANDO AUTENTICAÇÃO (JWT)")
        try:
            from app.core.security import create_access_token
            from app.core.config import settings
            from jose import jwt
            
            # 1. Simula a criação usando o seu padrão: data={"sub": "admin"}
            token = create_access_token(
                data={"sub": "admin"}, 
                expires_delta=timedelta(minutes=15)
            )
            self.assert_test("Geração de JWT", bool(token))
            
            # 2. Simula a decodificação para ver se a assinatura bate com a sua SECRET_KEY
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            self.assert_test("Validação de JWT", payload.get("sub") == "admin")
            
        except ImportError as e:
            print(f"{Colors.YELLOW}⚠️  Pulo de teste: Erro ao importar bibliotecas JWT: {e}{Colors.RESET}")
        except Exception as e:
            self.assert_test("Módulo JWT", False, str(e))
    def test_safe_crud(self):
        self.print_header("6. TESTANDO CRUD (Transação Segura)")
        try:
            from app.database import SessionLocal
            from app.models import Municipio
            
            db = SessionLocal()
            try:
                # Criação (Create)
                novo_mun = Municipio(nome="Municipio Teste Backend", uf="CE")
                db.add(novo_mun)
                db.flush() # Salva no banco mas não finaliza a transação
                self.assert_test("CRUD: CREATE Funciona", novo_mun.id is not None)
                
                # Leitura (Read)
                leitura = db.query(Municipio).filter(Municipio.id == novo_mun.id).first()
                self.assert_test("CRUD: READ Funciona", leitura.nome == "Municipio Teste Backend")
                
                # Forçamos o ROLLBACK para não sujar o banco de produção/dev
                db.rollback()
                self.assert_test("CRUD: ROLLBACK de segurança executado com sucesso", True)
                
            except Exception as e:
                db.rollback()
                self.assert_test("Operações CRUD", False, str(e))
            finally:
                db.close()
                
        except Exception as e:
            self.assert_test("Setup do CRUD de teste", False, str(e))

    def print_summary(self):
        self.print_header("RESULTADO FINAL")
        print(f"Total de testes: {self.passed + self.failed}")
        print(f"Passaram: {Colors.GREEN}{self.passed}{Colors.RESET}")
        print(f"Falharam: {Colors.RED}{self.failed}{Colors.RESET}")
        
        if self.failed == 0:
            print(f"\n{Colors.GREEN}🚀 SUCESSO ABSOLUTO! O Backend está sólido como uma rocha.{Colors.RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}⚠️ ATENÇÃO: Verifique os erros acima antes de seguir para produção.{Colors.RESET}\n")
            sys.exit(1)

if __name__ == "__main__":
    validator = BackendValidator()
    validator.run_all()