import sys
import os

# Adiciona o diretório raiz ao path para os imports funcionarem
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_current_user
from app.models import Usuario

# Cria um "navegador virtual" para testar a nossa API
client = TestClient(app)

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def run_integration_tests():
    print(f"\n{Colors.YELLOW}🚀 INICIANDO TESTES DE INTEGRAÇÃO AUTOMATIZADOS...{Colors.RESET}\n")

    # ==========================================================
    # TESTE 1: MUNDO REAL (Banco de Dados e GET público)
    # ==========================================================
    response = client.get("/api/municipios/")
    if response.status_code == 200:
        municipios = response.json()
        print(f"{Colors.GREEN}✅ [MUNDO REAL] GET /api/municipios/ acessado com sucesso.{Colors.RESET}")
        if len(municipios) > 0:
            print(f"   -> Banco já possui {len(municipios)} municípios cadastrados (Seed OK).")
        else:
            print(f"   -> {Colors.YELLOW}Aviso: Banco está vazio. Rode o 'popular_dados.py' depois.{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ [MUNDO REAL] Falha ao acessar municípios: {response.status_code}{Colors.RESET}")

    # ==========================================================
    # TESTE 2: O GUARDIÃO (Tentativa de acesso sem Autenticação)
    # ==========================================================
    payload_teste = {
        "mes": 12, "ano": 2099, "categoria": "PET", "peso_kg": 150.5, "associacao_id": 1
    }
    
    response_auth = client.post("/api/producao/", json=payload_teste)
    if response_auth.status_code == 401:
        print(f"{Colors.GREEN}✅ [GUARDIÃO] Acesso bloqueado corretamente para usuário sem token (401 Unauthorized).{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ [GUARDIÃO] Falha! A API deixou passar sem login. Status: {response_auth.status_code}{Colors.RESET}")

    def mock_user_logado():
        return Usuario(id=999, username="robo_de_teste", role="admin")
    
    app.dependency_overrides[get_current_user] = mock_user_logado
    
    print(f"\n{Colors.YELLOW}Simulando o login de um gestor...{Colors.RESET}")
    
    # 👇 A CORREÇÃO ESTÁ AQUI: Criamos uma Associação fantasma no banco só para o teste passar
    from app.database import SessionLocal
    from app.models import Associacao
    db = SessionLocal()
    if not db.query(Associacao).filter(Associacao.id == 1).first():
        db.add(Associacao(id=1, nome="Associação Teste da Vacina"))
        db.commit()
    db.close()

    # Dispara o primeiro cadastro (Vai funcionar)
    res1 = client.post("/api/producao/", json=payload_teste)
    
    # Dispara EXATAMENTE o mesmo cadastro de novo (Aqui a Vacina vai agir!)
    res2 = client.post("/api/producao/", json=payload_teste)
    
    if res2.status_code == 400 and "Já existe um registro" in res2.text:
        print(f"{Colors.GREEN}✅ [VACINA] Bloqueio de duplicidade funcionou perfeitamente!{Colors.RESET}")
        print(f"   -> A API respondeu: {res2.json()['detail']}")
    elif res2.status_code == 201:
         print(f"{Colors.RED}❌ [VACINA] Falha! A API permitiu cadastrar duplicado!{Colors.RESET}")
    else:
         print(f"{Colors.RED}❌ [VACINA] Comportamento inesperado. Status: {res2.status_code} - {res2.text}{Colors.RESET}")

    app.dependency_overrides.clear()

if __name__ == "__main__":
    run_integration_tests()