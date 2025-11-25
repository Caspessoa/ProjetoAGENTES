# Simulação de Gestão de Recursos Hídricos (CrewAI + Ollama)

Este projeto implementa uma simulação multiagente local para gestão de recursos hídricos, envolvendo negociação entre produtores, fiscalização ambiental e regulação pública.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

1.  **Python 3.12** (Versões 3.13+ podem apresentar incompatibilidade).
2.  **Ollama** (Motor de execução de LLMs locais).
3.  **Modelo GPT-OSS**: Execute `ollama pull gpt-oss` no seu terminal.

## Instalação (PowerShell)

Siga estes passos para configurar o ambiente em uma nova máquina.

### 1. Configurar o Ambiente Virtual
Na raiz do projeto, crie e ative o ambiente virtual:

```powershell
# Cria a pasta .venv
python -m venv .venv

# Ativa o ambiente
.\.venv\Scripts\activate

# Se receber erro de script não assinado, execute:
Set-ExecutionPolicy RemoteSigned -Scope Process

# Por fim, confirme
```
### 2. Instalar Dependências
Com o ambiente ativo (.venv), instale as bibliotecas necessárias.

```powershell
# Na pasta raiz
# Opção A
pip install -r requirements.txt

# Opção B
pip install "crewai[tools]==1.2.1" litellm python-dotenv
```

### 3. Configurar Variáveis de Ambiente
Certifique-se de que existe um arquivo `.env` no projeto (CrewAI) com o seguinte conteúdo:

```
MODEL=ollama/gpt-oss
API_BASE=http://localhost:11434
OPENAI_API_KEY=NA
```

### 4. Verificar Arquivos de Dados
Garanta que os seguintes arquivos de texto existam na raiz do projeto para alimentar o contexto dos agentes:

`lei_municipal.txt`

`tabela_agricultor.txt`

`tabela_empresario.txt`

`contexto_pesquisa_web.txt`

### 5. Como Rodar a Simulação
Certifique-se de que o Ollama está rodando (`ollama serve`).

No terminal (com o `.venv` ativo), navegue para a pasta de código fonte:
```
cd src

# Execute o módulo principal
python -m research_crew.main
```
#### Resultados
Ao final da execução:

O terminal exibirá o log de cada agente.

O tempo total de simulação será exibido.

Um relatório consolidado será salvo em `src/report.md`.
