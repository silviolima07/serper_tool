from crewai import Agent
from crewai_tools import SerperDevTool
#from app import modelo
import streamlit as st




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
        verbose=True,
        memory=True,
        tools=[serper_tool]
    )
    st.markdown("### Agente guia turistico sua mente sera o "+ str(modelo.model_name))
    return guia_turistico    
 
