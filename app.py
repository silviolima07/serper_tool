__import__("pysqlite3")  
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import pandas as pd
import streamlit as st
from crewai import Crew, Process
from my_agents import criar_agente_guia_turistico
from my_tasks import criar_task_recomendar
from MyLLM import MyLLM
import os
from PIL import Image
#import litellm  # Importando o LiteLLM para usar o Groq
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message="Overriding of current TracerProvider is not allowed")

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

trace.set_tracer_provider(TracerProvider())
trace.set_tracer_provider(None)


# Interface de Streamlit
html_page_title = """
    <div style="background-color:black;padding=60px">
        <p style='text-align:center;font-size:50px;font-weight:bold'>Próximo Destino</p>
    </div>
"""
st.markdown(html_page_title, unsafe_allow_html=True)

img = Image.open("img/travel.png")
st.sidebar.image(img, caption="", use_container_width=True)

st.sidebar.markdown("# Menu")
option = st.sidebar.selectbox("Menu", ["Pesquisar", 'About'], label_visibility='hidden')

if option == 'Pesquisar':
    st.markdown("### Selecione Estado:")
    estado = st.radio(
        "Estados possíveis:",
        ["Rio de Janeiro", "Bahia", "Pernambuco", "Ceará", "Santa Catarina"],
        horizontal=True
    )
    
    #st.markdown("### Quantas recomendações de lugares deseja:")
    #total_items = st.radio(" ", [1, 2, 3, 4, 5], horizontal=True)
    total_items = 3
    html_page_crewai = """
    <div style="background-color:black;padding=60px">
        <p style='text-align:center;font-size:40px;font-weight:bold'>Agents e Tasks</p>
    </div>
    """
    st.markdown(html_page_crewai, unsafe_allow_html=True)
    

    llm = MyLLM.GROQ_LLAMA
    guia_turistico = criar_agente_guia_turistico(llm)  # Passando o provider para o agente
    recomendar = criar_task_recomendar(guia_turistico)  # Passando o provider para a task
    
    st.markdown("## Aperte os cintos e boa viagem")
    
    # Certifique-se de que a Crew está configurada corretamente
    crew = Crew(
        agents=[guia_turistico],
        tasks=[recomendar],
        process=Process.sequential,  # Processamento sequencial das tarefas
        verbose=False,  # Verbose para depuração
        max_rpm=30,
        cache=True
    )
             
    col1, col2, col3 = st.columns(3)
    
    with col1:   
        st.markdown("### Top: " + str(total_items))
        st.markdown("### Estado: " + estado)
    
    with col2:
        if estado == 'Bahia':
            img_estado = Image.open("img/bahia.png")
        elif estado == 'Rio de Janeiro':
            img_estado = Image.open("img/rio_de_janeiro.png")
        elif estado == 'Ceará':
            img_estado = Image.open("img/ceara.png")
        elif estado == 'Santa Catarina':
            img_estado = Image.open("img/santa_catarina.png")  
        elif estado == 'Pernambuco':
            img_estado = Image.open("img/pernambuco.png")    
        
        st.image(img_estado, caption="", use_container_width=False)

    if st.button("INICIAR"):
        destino = "Pontos Turisticos"
        inputs = {
            'destino': destino,
            'continente': 'Brasil',
            'estado': estado,
            'url': 'pontos turisticos',
            'checar_url': "Não",
            'n_results': total_items
        }
        
        with st.spinner('Wait for it...searching and processing...wait please'):
            try:
                # Executa o Crew, o que deve agora acionar os agentes e tasks
                result = crew.kickoff(inputs=inputs)  # Faz a chamada ao crew.kickoff
                
                # Exibe a resposta no Streamlit
                st.markdown(f"### Resultado para {estado}")
                st.markdown(result)  # Função que processa e exibe a resposta
                
            except Exception as e:
                st.error(f"Error no crew.kickoff: {e}")
                
if option == 'About':
    st.markdown("### Quais pontos turisticos mais importantes num especifico Estado?")
    st.markdown("### Este aplicativo faz uma busca pelos Top lugares para conhecer.")
    st.markdown("### Modelo llama acessado via Groq.")

