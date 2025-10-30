#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path
import time  # <--- 1. IMPORTAMOS A BIBLIOTECA 'TIME'

# --- CARREGAR O .ENV ---
env_path = Path.cwd().parent / '.env'
load_dotenv(dotenv_path=env_path)

print(f"[Log: Tentando carregar .env de: {env_path}]")
if os.getenv("MODEL_NAME"):
    print(f"[Log: .env carregado com sucesso. MODEL_NAME={os.getenv('MODEL_NAME')}]")
else:
    print("[Log: AVISO! Não foi possível carregar MODEL_NAME do .env.]")

# --- IMPORTAR O CREW (COM NOME ATUALIZADO) ---
from research_crew.crew import SimulacaoRecursosHidricosCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Executa a simulação.
    """
    inputs = {
        'tema': 'Gestão de Recursos Hídricos na Bacia do Rio Piratini',
        'ano_atual': str(datetime.now().year)
    }
    
    print("[Log: Iniciando a simulação do Crew...]")
    
    # --- 2. REGISTRAMOS O TEMPO DE INÍCIO ---
    start_time = time.time()
    
    try:
        SimulacaoRecursosHidricosCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"Ocorreu um erro ao rodar o crew: {e}")
    
    # --- 3. CALCULAMOS E MOSTRAMOS O TEMPO DECORRIDO ---
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n\n==========================================")
    print("SIMULAÇÃO CONCLUÍDA.")
    print(f"[Log: Tempo total de simulação: {duration:.2f} segundos]") # <--- MOSTRA O TEMPO
    print(f"[Log: O sumário final foi salvo em 'report.md' na pasta 'src/']")
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
