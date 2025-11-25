# main.py (VERSÃO FINAL E MODERNA)
from crewai import Agent, Task, Crew, Process
# --- 1. IMPORTAÇÃO ATUALIZADA E CORRETA ---
# A classe agora se chama OllamaLLM e vem do novo pacote
from langchain_ollama import OllamaLLM

# --- 2. INSTÂNCIA DO LLM ATUALIZADA ---
# Usamos a nova classe. Como ela é específica para o Ollama,
# não precisamos mais do prefixo "ollama/" no nome do modelo.
ollama_llm = OllamaLLM(
    model="ollama/gpt-oss",
    base_url="http://localhost:11434"
)

# --- O RESTANTE DO CÓDIGO PERMANECE O MESMO ---

# Agente 1: Pesquisador
pesquisador = Agent(
  role='Pesquisador Especialista em IA',
  goal='Encontrar as tendências mais recentes e relevantes em Inteligência Artificial para 2025',
  backstory="""Você é um pesquisador renomado com um dom para identificar
  sinais em meio ao ruído. Seu conhecimento do cenário de IA é vasto e você é
  especialista em destilar informações complexas em conceitos compreensíveis.""",
  verbose=True,
  allow_delegation=False,
  llm=ollama_llm
)

# Agente 2: Escritor
escritor = Agent(
  role='Escritor Técnico Sênior',
  goal='Escrever um artigo de blog conciso e envolvente sobre as tendências de IA para 2025',
  backstory="""Você é um escritor aclamado, conhecido por sua habilidade de tornar
  tópicos técnicos acessíveis e interessantes para um público amplo.
  Você transforma jargões complexos em narrativas cativantes.""",
  verbose=True,
  allow_delegation=False,
  llm=ollama_llm
)

# Definição das Tarefas
tarefa_pesquisa = Task(
  description="""Conduza uma análise abrangente das últimas notícias, artigos de pesquisa e
  discussões de mercado para identificar as 3 principais tendências em IA para o ano de 2025.
  Concentre-se em avanços em áreas como IA Generativa, IA Explicável (XAI) e IA Ética.""",
  expected_output='Um relatório detalhado em formato de bullet points com as 3 principais tendências, cada uma com uma breve explicação.',
  agent=pesquisador
)

tarefa_escrita = Task(
  description="""Usando o relatório de pesquisa fornecido, escreva um artigo de blog de aproximadamente 500 palavras.
  O artigo deve ter um título cativante, uma introdução que prenda o leitor,
  e uma seção para cada uma das 3 tendências, explicando-as de forma clara.
  Conclua com uma breve reflexão sobre o futuro da IA.""",
  expected_output='O texto completo de um artigo de blog bem estruturado e pronto para publicação.',
  agent=escritor
)

# Montagem da "Trupe" e Execução
crew = Crew(
  agents=[pesquisador, escritor],
  tasks=[tarefa_pesquisa, tarefa_escrita],
  process=Process.sequential
)

print("========================================")
print("Iniciando a simulação da equipe de IA...")
print("========================================")
result = crew.kickoff()

print("\n\n========================================")
print("Simulação concluída! Resultado final:")
print("========================================")
print(result)