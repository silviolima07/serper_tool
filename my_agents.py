from crewai import Agent
from crewai_tools import SerperDevTool


import streamlit as st
from my_tools import url_checker_tool



# Initialize the tool for internet searching capabilities
serper_tool = SerperDevTool()

# Configuração do agente

def criar_agente_guia_turistico(modelo):
    
    guia_turistico = Agent(
        role="guia turistico",
        goal="Orientar pessoas que desejam viajar, conhecer novos lugares e recomendar os melhores destinos.",
        backstory=
            "Você é responsável por acompanhar e orientar visitantes em passeios turísticos."
            "Você ajuda oferecendo informações detalhadas sobre os pontos de interesse, a história local, aspectos culturais, e curiosidades sobre o destino. "
            "Você trabalha numa grande agência de viagens."
            "Você tem um conhecimento aprofundado dos lugares que visitam e ajudam os turistas a aproveitar ao máximo suas viagens, explicando a importância histórica ou cultural dos locais visitados."    
        ,
        llm=modelo,
        verbose=False,
        memory=False,
        tools=[serper_tool]
    )
    st.markdown("#### Agente guia turistico sua mente sera o "+ str(modelo.model_name))
    return guia_turistico    
 
# Fiz a inclusao das linhas pedindo para verificar o valor da variavel checar_url e passei o {checar_url}
# Mas nao adiantou nada.
 
def criar_agente_url_checker(modelo):
    url_checker_agent = Agent(
        role='URL Checker Agent',
        goal='Verificar se a URL fornecida está acessível',
        backstory="Variavel checar_url igual a {checar_url}. Se variavel checar_url igual a 'Sim', se for igual a 'Sim', você verifica se a conexão com a url do site esta ok",
        verbose=True,
        memory=False,
        max_iter=15,
        tools=[url_checker_tool],
        llm=modelo  # Não há necessidade de usar um modelo LLM aqui
    )
    st.markdown("#### Agente url_checker_agent criado.")
    return url_checker_agent