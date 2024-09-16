import pandas as pd
import streamlit as st
from crewai import Crew, Process
from my_agents import criar_agente_guia_turistico , criar_agente_url_checker
from my_tasks import criar_task_recomendar, criar_task_url_checker
from config_llm import llama
import os
from PIL import Image

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
# Suprimir avisos específicos
warnings.filterwarnings("ignore", message="Overriding of current TracerProvider is not allowed")


from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Definir um TracerProvider que não coleta dados
trace.set_tracer_provider(TracerProvider())

# Desabilitar o TracerProvider (basicamente sem definir um novo)
trace.set_tracer_provider(None)



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
    ["praias", "pontos turisticos"],
    captions=[
        "praias interessantes",
        "comemorações"],
     horizontal = True   
    )
    st.write("Destino selecionado:", destino.upper())
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

def selecionar_estado():
    estado = st.radio(
    "Estados possiveis:",
    ["Rio de Janeiro", "Bahia", "Pernambuco", "Ceará", "Santa Catarina"],
    horizontal = True
    )
    st.write("Estado selecionado:", estado)
    return estado    

html_page_title = """
     <div style="background-color:black;padding=60px">
         <p style='text-align:center;font-size:50px;font-weight:bold'>Próximo Destino</p>
     </div>
               """               
st.markdown(html_page_title, unsafe_allow_html=True)

img = Image.open("img/travel.png")
st.sidebar.image(img,caption="",use_column_width=True)

st.sidebar.markdown("# Menu")
option = st.sidebar.selectbox("Menu", ["Pesquisar", 'About'], label_visibility='hidden')

if option == 'Pesquisar':
    #st.markdown("## Selecione o destino desejado:")
    #destino = selecionar_destino()
    
    st.markdown("### Selecione Estado:")
    estado = selecionar_estado()
    
    #st.markdown("## Selecione continente:")
    #continente = selecionar_continente()
    
    st.markdown("### Quantas recomendações de lugares deseja:")
    total_items = st.radio(" ",[1,2,3,4,5], horizontal = True)
    
    #st.markdown("## Deseja checar a url da recomendação?")
    #checar_url = st.radio(
    #" ",
    #["Não", "Sim"],
    #captions=[
    #    "Mais rápido a resposta",
    #    "Exige mais processamento e pode demorar",
    #],
    #horizontal = True
    #)
    
    #if continente == 'Brasil':
    #st.markdown("## Selecione Estado:")
    #estado = selecionar_estado()
    #st.markdown("## Agents e Tasks")
    
    html_page_crewai = """
     <div style="background-color:black;padding=60px">
         <p style='text-align:center;font-size:40px;font-weight:bold'>Agents e Tasks</p>
     </div>
               """               
    st.markdown(html_page_crewai, unsafe_allow_html=True)
    
    # Configuração da crew com o agente guia turistico
    modelo = llama
    guia_turistico = criar_agente_guia_turistico(modelo)
    # Cria a task usando o agente criado
    recomendar = criar_task_recomendar(guia_turistico)
    st.write(" ")
    # Cria agente para checar se url esta ok
    #url_checker_agent = criar_agente_url_checker(modelo)
    # Cria a task usando o agente criado
    #url_checker_task = criar_task_url_checker(url_checker_agent)
    
    st.write(" ")  
        
    st.markdown("## Aperte os cintos e boa viagem")
    st.write(" ") 
    
    crew = Crew(
                agents=[guia_turistico],# url_checker_agent],
                tasks=[recomendar],# url_checker_task],
                process=Process.sequential,  # Processamento sequencial das tarefas
                verbose=False,
                max_rpm=30
             )
             
    col1, col2, col3 = st.columns(3)
    
    
   
    with col1:   
        #st.markdown("### Partiu: "+ destino)
        #st.markdown("### Local: "+ continente)
        #st.markdown("### Checar url: "+ checar_url)
        st.markdown("### Top: "+ str(total_items))
        #if continente == 'Brasil':
        st.markdown("### Estado: "+ estado)
            
    with col2:
        if estado == 'Bahia':
            img_estado = Image.open("img/bahia.png")
            #st.write("Elevador Lacerda")
        
        elif estado == 'Rio de Janeiro':
             img_estado = Image.open("img/rio_de_janeiro.png")
             #st.write("Cristo Redentor")
             
        elif estado == 'Ceará':
             img_estado = Image.open("img/ceara.png")
             #st.write("Canoa Quebrada")
             
        elif estado == 'Santa Catarina':
             img_estado = Image.open("img/santa_catarina.png")  
             #st.write("Vale das Águas")             
             
        elif estado == 'Pernambuco':
             img_estado = Image.open("img/pernambuco.png")    
             #st.write("Bonito")             
        
        st.image(img_estado,caption="",use_column_width=False)        
            
        
        
        

    if st.button("INICIAR"):
        #if continente == 'Brasil':
        #    inputs = {'destino': destino,
        #          'continente': continente,
        #          'regiao': regiao,
        #          'url': 'skylinewebcams.com'}
        #else:
        destino = "Pontos Turisticos"
        continente = 'Brasil'
        inputs = {'destino': destino,
                  'continente': continente,
                  'estado': estado,
                  'url': 'pontos turisticos', #'skylinewebcams.com',
                  'checar_url': "Não", #checar_url,
                  'n_results':total_items}
           
        with st.spinner('Wait for it...searching and processing...wait please'):
            # Executa o CrewAI
            try:
                result = crew.kickoff(inputs=inputs)               
                
                html_page_result = """
     <div style="background-color:black;padding=60px">
         <p style='text-align:center;font-size:40px;font-weight:bold'>Resultado</p>
     </div>
               """               
                st.markdown(html_page_result, unsafe_allow_html=True)
                
                #st.markdown("##### Fonte: https://www.skylinewebcams.com/")
                #st.markdown("##### Os links não foram testados e as câmeras podem estar offline.")
                st.markdown("## Pontos Turisticos")
                st.write(result.raw)
                
                
            except:
                 st.write("error no crew.kickoff")
                
            
                
if option == 'About':
    #st.markdown("# About:")
    st.markdown("### Este aplicativo faz uma busca usando a API SERP.")
    st.markdown("### Um agente guia turistico efetua uma busca baseada nos critérios definidos pelo usuário.")
    #st.markdown("### O site skylinewebcams é acessado pelo agente para pesquisar o destino desejado.")
    #st.markdown("### Nem todos links estão ok, pois o site não atualizou as câmeras cadastradas." )
    st.markdown("### Modelo acessado via Groq.")
    #st.markdown("### Exemplo de resposta do agente Guia Turistico:")    
    #"""
    #1. **Copacabana - Rio de Janeiro**
#Comentário: Esta praia é um dos cartões-postais do Brasil, com suas águas calmas e areia branca. A infraestrutura turística é muito bem desenvolvida, com hotéis, restaurantes e bares ao longo da orla. É um local ideal para visitar durante o verão, de dezembro a março.
#    """    
