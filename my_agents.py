from crewai import Agent
from crewai_tools import SerperDevTool
import litellm

import streamlit as st
from my_tools import url_checker_tool

# Defina a função do provedor Groq
def groq_provider():
    return litellm.completion(
        model="groq/llama3-8b-8192",  # Certifique-se de que este é o modelo correto do Groq
        messages=[
            {"role": "system", "content": "Você é um guia turístico especializado."},
            {"role": "user", "content": "Recomende os melhores pontos turísticos do Brasil."}
        ],
        #type="chat",
        tools=[],
        tool_choice="auto"
    )

# Initialize the tool for internet searching capabilities
serper_tool = SerperDevTool()

# Configuração do agente

def criar_agente_guia_turistico(provider):
    
    guia_turistico = Agent(
        role="guia turistico",
        goal="Orientar pessoas que desejam viajar, conhecer novos lugares e recomendar os melhores destinos.",
        backstory=
            "Você é responsável por acompanhar e orientar visitantes em passeios turísticos."
            "Você ajuda oferecendo informações detalhadas sobre os pontos de interesse, a história local, aspectos culturais, e curiosidades sobre o destino. "
            "Você trabalha numa grande agência de viagens."
            "Você tem um conhecimento aprofundado dos lugares que visitam e ajudam os turistas a aproveitar ao máximo suas viagens, explicando a importância histórica ou cultural dos locais visitados."    
        ,
        llm=provider, # estava provider=provider
        verbose=True,
        memory=True,
        tools=[serper_tool]
    )
    #st.markdown("#### Agente guia turistico sua mente sera o "+ str(provider.model))
    return guia_turistico    
 
# Fiz a inclusao das linhas pedindo para verificar o valor da variavel checar_url e passei o {checar_url}
# Mas nao adiantou nada.
 
def criar_agente_url_checker(provider):
    url_checker_agent = Agent(
        role='URL Checker Agent',
        goal='Verificar se a URL fornecida está acessível',
        backstory="Variavel checar_url igual a {checar_url}. Se variavel checar_url igual a 'Sim', se for igual a 'Sim', você verifica se a conexão com a url do site esta ok",
        verbose=True,
        memory=False,
        max_iter=15,
        tools=[url_checker_tool],
        llm=provider  # Não há necessidade de usar um modelo LLM aqui
    )
    st.markdown("#### Agente url_checker_agent criado.")
    return url_checker_agent