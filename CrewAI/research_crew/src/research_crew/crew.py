# src/research_crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class SimulacaoRecursosHidricosCrew():
    """SimulacaoRecursosHidricos crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml' # Verifique se não há erro de digitação aqui

    # --- CARREGANDO OS 6 AGENTES ---
    @agent
    def regulador_prefeito(self) -> Agent:
        return Agent(config=self.agents_config['regulador_prefeito'], verbose=True)

    @agent
    def regulador_vereador(self) -> Agent:
        return Agent(config=self.agents_config['regulador_vereador'], verbose=True)

    @agent
    def fiscalizador_fiscal(self) -> Agent:
        return Agent(config=self.agents_config['fiscalizador_fiscal'], verbose=True)

    @agent
    def fiscalizador_ong(self) -> Agent:
        return Agent(config=self.agents_config['fiscalizador_ong'], verbose=True)

    @agent
    def produtor_agricultor(self) -> Agent:
        return Agent(config=self.agents_config['produtor_agricultor'], verbose=True)

    @agent
    def produtor_empresario(self) -> Agent:
        return Agent(config=self.agents_config['produtor_empresario'], verbose=True)

    # --- 1. ADICIONAMOS O NOVO AGENTE RELATOR ---
    @agent
    def relator_geral(self) -> Agent:
        return Agent(config=self.agents_config['relator_geral'], verbose=True)

    # --- CARREGANDO AS TAREFAS ---
    @task
    def tarefa_producao_negociacao(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_producao_negociacao'],
            agent=self.produtor_agricultor() 
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

    # --- 2. ADICIONAMOS A NOVA TAREFA DE SUMÁRIO ---
    @task
    def tarefa_sumario_geral(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_sumario_geral'],
            agent=self.relator_geral() # Atribuímos ao novo agente
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SimulacaoRecursosHidricos crew"""
        return Crew(
            # --- 3. ADICIONAMOS O NOVO AGENTE À LISTA ---
            agents=[
                self.regulador_prefeito(),
                self.regulador_vereador(),
                self.fiscalizador_fiscal(),
                self.fiscalizador_ong(),
                self.produtor_agricultor(),
                self.produtor_empresario(),
                self.relator_geral() # <--- NOVO AGENTE AQUI
            ],
            # --- 4. ADICIONAMOS A NOVA TAREFA AO FINAL DA FILA ---
            tasks=[
                self.tarefa_producao_negociacao(),
                self.tarefa_fiscalizacao(),
                self.tarefa_relatorio_ong(),
                self.tarefa_politica_reguladores(),
                self.tarefa_sumario_geral() # <--- NOVA TAREFA AQUI
            ],
            process=Process.sequential,
            verbose=True
        )