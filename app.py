import pandas as pd
import streamlit as st
from crewai import Crew, Process
from my_agents import criar_agente_guia_turistico , criar_agente_url_checker
from my_tasks import criar_task_recomendar, criar_task_url_checker
from config_llm import llama
import os
from PIL import Image

def clean_lista_resultado():
    temp = []
    with open("lista_resultado.txt", "r") as arquivo:
	    texto  = arquivo.read()
    for line in texto:
        if line.startswith('Link'):
            st.write(line)
    
    
def selecionar_destino():
    destino = st.radio(
    "Destinos possiveis:",
    ["praias", "parques", "festas"],
    captions=[
        "praias interessantes",
        "lugares preservados",
        "comemorações"],
     horizontal = True   
    )
    st.write("Destino selecionado:", destino)
    return destino
    
def selecionar_continente():
    continente = st.radio(
    "Continentes possiveis:",
    ["Brasil", "Americas", "Europa", "Africa", "Asia", "Oceania"],
    captions=[
        "Apenas Brasil",
        "22 paises nas Americas",
        "25 paises na Europa",
        "7 paises na Africa",
        "10 paises na Asia",
        "Australia"],
    horizontal = True
    )
    st.write("Continente selecionado:", continente)
    return continente

def selecionar_regiao():
    regiao = st.radio(
    "Regioes possiveis:",
    ["Norte", "Sul", "Nordeste", "Centro-Oeste", "Sudeste"],
    horizontal = True
    )
    st.write("Regiao selecionada:", regiao)
    return regiao    

html_page_title = """
     <div style="background-color:black;padding=60px">
         <p style='text-align:center;font-size:50px;font-weight:bold'>Janela do Mundo</p>
     </div>
               """               
st.markdown(html_page_title, unsafe_allow_html=True)

img = Image.open("img/travel.png")
st.sidebar.image(img,caption="",use_column_width=True)

st.sidebar.markdown("# Menu")
option = st.sidebar.selectbox("Menu", ["Pesquisar", 'About'], label_visibility='hidden')

if option == 'Pesquisar':
    st.markdown("## Selecione um destino desejado:")
    destino = selecionar_destino()
    
    st.markdown("## Selecione continente:")
    continente = selecionar_continente()
    
    st.markdown("## Quantas recomendações deseja (3 a 6):")
    total_items = st.slider(" ", 3, 6)
    
    checar_url = st.radio(
    "Deseja checar a url da recomendação?",
    ["Não", "Sim"],
    captions=[
        "Mais rápido a resposta",
        "Exige mais processamento e pode demorar",
    ],
)
    
    #if continente == 'Brasil':
    #    regiao = selecionar_regiao()
    st.markdown("## Agents e Tasks")
    # Configuração da crew com o agente guia turistico
    modelo = llama
    guia_turistico = criar_agente_guia_turistico(modelo)
    # Cria a task usando o agente criado
    recomendar = criar_task_recomendar(guia_turistico)
    st.write(" ")
    # Cria agente para checar se url esta ok
    url_checker_agent = criar_agente_url_checker(modelo)
    # Cria a task usando o agente criado
    url_checker_task = criar_task_url_checker(url_checker_agent)
    
    st.write(" ")  
        
    st.markdown("## Aperte os cintos e boa viagem")
    st.write(" ") 
    
    crew = Crew(
                agents=[guia_turistico, url_checker_agent],
                tasks=[recomendar, url_checker_task],
                process=Process.sequential,  # Processamento sequencial das tarefas
                verbose=False
             )
             
    col1, col2, col3 = st.columns(3)
    
    
   
    with col1:   
        st.markdown("### Partiu: "+ destino)
        st.markdown("### Local: "+ continente)
        st.markdown("### Checar url: "+ checar_url)
        st.markdown("### Top: "+ str(total_items))
        #if continente == 'Brasil':
        #    st.markdown("### Regiao: "+ regiao)
            
    with col2:
        if destino == 'praias':
            img_destino = Image.open("img/jeri.png")
            st.write("Jericoacora")
        
        elif destino == 'parques':
             img_destino = Image.open("img/parque.png")
        else:
             img_destino = Image.open("img/parintins_300.png")    
             st.write("Parintins")             
        
        st.image(img_destino,caption="",use_column_width=False)        
            
        
        
        

    if st.button("INICIAR"):
        #if continente == 'Brasil':
        #    inputs = {'destino': destino,
        #          'continente': continente,
        #          'regiao': regiao,
        #          'url': 'skylinewebcams.com'}
        #else:
        inputs = {'destino': destino,
                  'continente': continente,
                  'url': 'skylinewebcams.com',
                  'checar_url': checar_url,
                  'n_results':total_items}
           
        with st.spinner('Wait for it...'):
            # Executa o CrewAI
            try:
                result = crew.kickoff(inputs=inputs)
                st.markdown("## Resultado:")
                st.markdown("##### Os links podem ter sido checados ou não e as câmeras podem estar offline.")
                st.write(result.raw)
                
                
            except:
                 st.write("error no crew.kickoff")
                
            
                
if option == 'About':
    #st.markdown("# About:")
    st.markdown("### Este aplicativo faz uma busca usando a API SERP.")
    st.markdown("### Um agente guia turistico efetua uma busca baseada nos critérios definidos pelo usuário.")
    st.markdown("### O site skylinewebcams é acessado pelo agente para pesquisar o destino desejado.")
    st.markdown("### Nem todos links estão ok, pois o site não atualizou as câmeras cadastradas." )
    st.markdown("### Modelo acessado via Groq.")
    st.markdown("### Exemplo de resposta do agente Guia Turistico")    
    """
    1. **Copacabana - Rio de Janeiro**
Link: https://www.skylinewebcams.com/en/webcam/brasil/rio-de-janeiro/rio-de-janeiro/copacabana.html
Comentário: Esta praia é um dos cartões-postais do Brasil, com suas águas calmas e areia branca. A infraestrutura turística é muito bem desenvolvida, com hotéis, restaurantes e bares ao longo da orla. É um local ideal para visitar durante o verão, de dezembro a março.
    """    
