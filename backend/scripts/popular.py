import subprocess
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


SCRIPTS = [
    "popular_associacoes.py", 
    "popular_grupos.py",       
    "popular_municipios.py",       
    "popular_producao.py",    
]

print("🚀 INICIANDO PIPELINE DE POPULARIZAÇÃO DO BANCO...")
print("="*70)

for script in SCRIPTS:
    script_path = os.path.join(BASE_DIR, script)
    

    if not os.path.exists(script_path):
        print(f"\n⚠️ AVISO: Script não encontrado: {script}. Pulando...")
        continue

    print(f"\n⏳ [PIPELINE] Rodando -> {script}")
    print("-" * 50)
    
    try:

        subprocess.run([sys.executable, script_path], check=True)
        print("-" * 50)
        print(f"✅ [PIPELINE] {script} finalizado com sucesso!")
        
    except subprocess.CalledProcessError:
        print("\n❌ ERRO FATAL: Ocorreu um problema no meio do caminho.")
        print(f"🛑 Pipeline interrompido no script '{script}' para evitar quebra no banco de dados.")
        sys.exit(1) 

print("\n" + "="*70)
print("🎉 PIPELINE TOTALMENTE CONCLUÍDO! O seu banco está 100% populado.")
print("="*70)