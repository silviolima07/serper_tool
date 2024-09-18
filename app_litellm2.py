from crewai import Agent
from litellm import completion
from config_llm import groq_provider

import streamlit as st

# Criando o agente de guia turístico
guia_turistico = Agent(
    role="Guia Turístico Especializado",
    goal="Oferecer as melhores recomendações de viagem baseadas nos interesses do viajante.",
    backstory="Você é um guia turístico com décadas de experiência, conhecendo os melhores lugares para visitar.",
    provider=groq_provider(),  # Usando o provider Groq
    verbose=True,
    llm='groq/llama3-8b-8192'
)
from crewai import Task

# Definindo a task para recomendar os melhores destinos turísticos
recomendar_task = Task(
    description="""
    Como guia turístico especializado, sua tarefa é analisar as opções de viagem disponíveis e recomendar os melhores destinos baseados em clima, eventos e custo.
    Seu relatório final deve incluir:
    - Análise das condições climáticas.
    - Sugestão de locais turísticos.
    - Custos aproximados de viagem.
    """,
    expected_output="Um relatório completo sobre os melhores destinos turísticos, incluindo clima e custos.",
    agent=guia_turistico
)

from crewai import Crew, Process

# Criando o crew com o agente de guia turístico e a task de recomendação
crew = Crew(
    agents=[guia_turistico],
    tasks=[recomendar_task],
    process=Process.sequential,  # Processamento sequencial das tarefas
    verbose=True
)

# Executando o CrewAI com os inputs necessários
inputs = {
    'destino': 'Pontos Turísticos',
    'estado': 'Bahia',
    'interesses': 'Natureza, Cultura'
}

# Executando o crew e processando as tarefas
#result = crew.kickoff(inputs=inputs)

# Exibindo o resultado da execução
with st.spinner('Wait for it...searching and processing...wait please'):
    try:
        # Executa a tarefa
        result = crew.kickoff(inputs=inputs)

        # Exibe o resultado completo para análise
        st.write("Resultado")
        st.write(result.raw)

        # Verifica se 'tasks_output' está presente e contém elementos
        #if 'tasks_output' in result and len(result['tasks_output']) > 0:
            # Acessa o primeiro item em 'tasks_output'
            #task_output = result['tasks_output'][0]
        
            # Verifica se task_output é um objeto e possui a propriedade 'description'
            #if isinstance(task_output, dict) and 'description' in task_output:
            #    content = task_output['description']
            #    st.markdown(content)  # Usa markdown para exibir o conteúdo formatado
            #else:
                #st.error("O item em 'tasks_output' não contém a descrição esperada.")
        #else:
        #    st.error("A resposta não contém 'tasks_output' ou está vazio.")
        
    except Exception as e:
        st.error(f"Error no crew.kickoff: {e}")
