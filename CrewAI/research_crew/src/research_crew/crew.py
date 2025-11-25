# src/research_crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# --- 1. REMOVER A IMPORTAÇÃO DA FERRAMENTA ---
# from research_crew.tools.custom_tool import search_tool

@CrewBase
class SimulacaoRecursosHidricosCrew():
    """SimulacaoRecursosHidricos crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml' 

    # --- AGENTES ---
    @agent
    def regulador_prefeito(self) -> Agent:
        return Agent(config=self.agents_config['regulador_prefeito'], verbose=True)

    @agent
    def regulador_vereador(self) -> Agent:
        return Agent(config=self.agents_config['regulador_vereador'], verbose=True)

    @agent
    def relator_geral(self) -> Agent:
        return Agent(config=self.agents_config['relator_geral'], verbose=True)

    @agent
    def fiscalizador_fiscal(self) -> Agent:
        return Agent(config=self.agents_config['fiscalizador_fiscal'], verbose=True)

    @agent
    def fiscalizador_ong(self) -> Agent:
        return Agent(
            config=self.agents_config['fiscalizador_ong'],
            # tools=[search_tool], # <-- 2. REMOVER A FERRAMENTA
            verbose=True
        )

    @agent
    def produtor_agricultor(self) -> Agent:
        return Agent(config=self.agents_config['produtor_agricultor'], verbose=True)

    @agent
    def produtor_empresario(self) -> Agent:
        return Agent(config=self.agents_config['produtor_empresario'], verbose=True)

    # --- TAREFAS ---
    @task
    def tarefa_oferta_agricultor(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_oferta_agricultor'],
            agent=self.produtor_agricultor() 
        )

    @task
    def tarefa_resposta_empresario(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_resposta_empresario'],
            agent=self.produtor_empresario() 
        )

    @task
    def tarefa_fiscalizacao(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_fiscalizacao'],
            agent=self.fiscalizador_fiscal()
        )
    
    @task
    def tarefa_relatorio_ong(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_relatorio_ong'],
            agent=self.fiscalizador_ong()
        )

    @task
    def tarefa_politica_reguladores(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_politica_reguladores'],
            agent=self.regulador_prefeito() 
        )

    @task
    def tarefa_sumario_geral(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_sumario_geral'],
            agent=self.relator_geral()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SimulacaoRecursosHidricos crew"""
        return Crew(
            agents=self.agents, # type: ignore[attr-defined]
            tasks=self.tasks, # type: ignore[attr-defined]
            process=Process.sequential,
            verbose=True
            # 3. REMOVER A 'tools=[]' DAQUI
        )