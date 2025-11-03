#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path
import time 

# --- CARREGAR O .ENV ---
env_path = Path.cwd().parent / '.env'
load_dotenv(dotenv_path=env_path)

print(f"[Log: Tentando carregar .env de: {env_path}]")
if os.getenv("MODEL_NAME"):
    print(f"[Log: .env carregado com sucesso. MODEL_NAME={os.getenv('MODEL_NAME')}]")
else:
    print("[Log: AVISO! Não foi possível carregar MODEL_NAME do .env.]")

# --- IMPORTAR O CREW ---
from research_crew.crew import SimulacaoRecursosHidricosCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# --- FUNÇÃO HELPER PARA CARREGAR ARQUIVOS ---
def carregar_arquivo_referencia(file_path: str) -> str:
    """Lê um arquivo de referência da raiz do projeto."""
    try:
        caminho_completo = Path.cwd().parent / file_path
        if not caminho_completo.exists():
            return f"ERRO: Arquivo de referência '{file_path}' não encontrado."
        with open(caminho_completo, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERRO ao ler '{file_path}': {str(e)}"

def run():
    """
    Executa a simulação.
    """
    
    # --- 1. CARREGAR OS DADOS ANTES DA SIMULAÇÃO ---
    tabela_agricultor = carregar_arquivo_referencia("tabela_agricultor.txt")
    tabela_empresario = carregar_arquivo_referencia("tabela_empresario.txt")
    lei_municipal = carregar_arquivo_referencia("lei_municipal.txt")
    pesquisa_ong = carregar_arquivo_referencia("contexto_pesquisa_web.txt") # <-- NOVO

    # --- 2. INJETAR OS DADOS NOS INPUTS ---
    inputs = {
        'tema': 'Gestão de Recursos Hídricos na Bacia do Rio Piratini',
        'ano_atual': str(datetime.now().year),
        'conteudo_tabela_agricultor': tabela_agricultor,
        'conteudo_tabela_empresario': tabela_empresario,
        'conteudo_lei_municipal': lei_municipal,
        'conteudo_pesquisa_web': pesquisa_ong # <-- NOVO
    }
    
    print("[Log: Iniciando a simulação do Crew...]")
    
    start_time = time.time()
    crew_result = None # Inicializa a variável
    
    try:
        crew_result = SimulacaoRecursosHidricosCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        # --- 3. CORREÇÃO DO RECURSIONERROR ---
        # Capturamos o erro e o imprimimos de forma simples,
        # fora do print() que causa o crash do 'rich'.
        print(f"\n\n[ERRO NA EXECUÇÃO DO CREW]: {str(e)}\n\n")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n\n==========================================")
    print("SIMULAÇÃO CONCLUÍDA.")
    print(f"[Log: Tempo total de simulação: {duration:.2f} segundos]")
    
    if crew_result:
        print(f"[Log: O sumário final foi salvo em 'report.md' na pasta 'src/']")
    else:
        print("[Log: A simulação falhou e não gerou um relatório final.]")
        
    print("============================================")
    
if __name__ == "__main__":
    run()
    
def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        SimulacaoRecursosHidricosCrew().crew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SimulacaoRecursosHidricosCrew().crew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        SimulacaoRecursosHidricosCrew().crew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = SimulacaoRecursosHidricosCrew().crew().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
