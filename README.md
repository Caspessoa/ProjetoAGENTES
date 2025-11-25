# ProjetoAGENTES
Repositório voltado ao Projeto de Sistemas Multiagente da Universidade Federal de Pelotas (UFPEL)

# 📄 Dossiê Técnico: Simulação Multiagente de Recursos Hídricos com LLMs Locais

**Data:** 25 de Novembro de 2025

**Status:** Funcional (Versão 1.0 - Injeção de Contexto)

**Objetivo:** Validar arquitetura para simulação de sistemas multiagente (MAS) rodando 100% localmente, visando comparação futura entre frameworks (CrewAI vs. AutoGen).

## 1. Stack Tecnológico Definido

Após testes de compatibilidade e depuração, o ambiente estável foi definido como:

| Componente | Escolha | Justificativa / Notas |
| :--- | :--- | :--- |
| **Linguagem** | **Python 3.12** | Versões mais novas (3.13) apresentaram incompatibilidade com bibliotecas de IA essenciais. |
| **Motor de LLM** | **Ollama** | Execução local eficiente. Permite troca rápida de modelos e exposição via API local. |
| **Modelo Base** | **GPT-OSS** | Modelo alvo do estudo. Demonstrou boa capacidade de raciocínio em contexto, mas limitações com uso autônomo de ferramentas (*Tool Calling*). |
| **Framework** | **CrewAI (v1.2.1)** | Escolhido pela estrutura hierárquica de agentes. A versão 1.2.1 foi mantida devido a restrições do `pyproject.toml` original. |
| **Conector** | **LiteLLM** | Biblioteca nativa usada pelo CrewAI v1.2.1 para conectar ao Ollama via variáveis de ambiente. |

## 2. Histórico de Decisões e Pivôs Arquiteturais

### A. Do TinyTroupe para CrewAI
Inicialmente, explorou-se o *Microsoft TinyTroupe*. O framework mostrou-se frágil para ambientes locais customizados, com dependências rígidas de APIs proprietárias (OpenAI/Azure). A migração para o **CrewAI** ofereceu melhor suporte a LLMs locais via Ollama.

### B. O Desafio do "Tool Calling" com Modelos de Base
Durante o desenvolvimento, identificou-se que o modelo **GPT-OSS** falhava consistentemente (`Invalid response - None`) ao tentar executar ações de "ReAct" complexas, como decidir autonomamente usar uma ferramenta de leitura de arquivo ou busca na web.

**Solução Adotada: Estratégia de Injeção de Contexto**
Para viabilizar a simulação com o modelo alvo, alterou-se a arquitetura:
* **Antes (Falha):** O Agente recebia uma ferramenta e a instrução "Use a ferramenta para ler o arquivo X".
* **Depois (Sucesso):** O script principal (`main.py`) lê os arquivos preliminarmente e injeta o conteúdo bruto diretamente no prompt da tarefa (`tasks.yaml`). Isso transformou um problema de *execução* em um problema de *raciocínio*, onde o GPT-OSS excela.

## 3. Arquitetura da Solução

### Estrutura de Pastas
```text
research_crew/
├── .env                  # Configuração do Modelo (MODEL, API_BASE)
├── lei_municipal.txt     # Base de Conhecimento (Regras)
├── tabela_agricultor.txt # Base de Conhecimento (Produtor 1)
├── tabela_empresario.txt # Base de Conhecimento (Produtor 2)
├── contexto_pesquisa.txt # Base de Conhecimento (ONG)
└── src/
    └── research_crew/
        ├── main.py       # Orquestrador: Carrega .env, lê arquivos .txt, injeta nos inputs e inicia
        ├── crew.py       # Definição: Instancia Agentes e Tarefas, monta a Equipe
        ├── config/
        │   ├── agents.yaml # Personas (Roles, Goals, Backstories)
        │   └── tasks.yaml  # Instruções e Templates ({conteudo_tabela...})
```
### Fluxo de Dados (Pipeline)
1. **Inicialização**: `main.py` carrega variáveis de ambiente e lê arquivos `.txt` do disco.

2. **Injeção**: Os textos lidos são passados como dicionário `inputs` para o `kickoff()` do Crew.

3. **Execução Sequencial**:
* O Agente recebe o prompt com os dados já inclusos.
* O Agente processa a informação e gera uma saída em texto simples.
* A saída é passada como contexto para o próximo Agente.

4. **Consolidação**: O Agente Relator compila todas as interações em um `report.md` final.

## 4. Próximos Passos (Roteiro Futuro)
Para a evolução do projeto e comparação com AutoGen:

1. **Implementação de Estado (Statefulness):** Desenvolver lógica Python para persistir variáveis (saldo financeiro, nível de poluição acumulado) entre rodadas de simulação, superando a limitação atual onde os valores são apenas "simulados" em texto.

2. **Migração para CrewAI v2.0 (Flows):** Atualizar o framework para permitir execução paralela (ex: ONG e Fiscal trabalhando simultaneamente) e loops de feedback.

3. **Comparativo com AutoGen:** Replicar o cenário utilizando o framework da Microsoft para testar a autonomia conversacional sem roteiro linear rígido.
