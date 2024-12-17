from crewai import Task
import streamlit as st

from pydantic import BaseModel
from typing import List

class RecomendaOuput(BaseModel):
    recomendacoes: List[str]




def criar_task_recomendar(guia_turistico):
    recomendar = Task(
        description=(
             "Usar a ferramenta de busca para pesquisar por {url} sobre {destino} no {continente} Estado {estado}, numero de resultados maximo igual a {n_results}."
             "Executar a pesquisa somente por {url}."
             "Ao encontrar {n_results} recomendações aplicar a classificação."
             "Critérios de classificação: beleza natural e a infraestrutura turística entre os turistas."             
             "Faça sempre em Português do Brasil (pt-br)."
             "Sempre incluir comentários de cada local recomendando os melhores meses para visitar."
            "Resposta na forma de tabela com as colunas: Ponto Turístico, Classificação, Melhores meses para visitar, Temperatura média, Média de gasto por dia"
             "Um item por linha.") ,
        expected_output=
             #"Lista dos lugares encontrados com comentários a respeito de cada local." # Não incluir a url do link da página do site se variavel checar_url for igual a 'Não'."
             """ 
#Usar fonte tamanho medio e dar espaço de uma linha nas respostas. 
#Um relatório detalhado dos pontos turisticos com:            
#1 - Classificação segundo os critérios definidos ;
#2 - Melhores meses para visitar;
#3 - Temperatura média nos melhores meses para visitar;
#4 - Média de gasto por dia, considerando um almoço e passeios;
Exemplo de saida esperada:
Ponto Turístico	Classificação	Melhores meses para visitar	Temperatura média	Média de gasto por dia
Parque Nacional da Tijuca	9/10	Inverno e primavera	23°C	20R$\n
Praia de Copacabana	8/10	Verão e inverno	26°C	45R$\n
Parque Lage	8,5/10	Primavera e inverno	25°C	25R$
"""
         ,
         agent=guia_turistico,
         output_file='lista_resultado'
         #provider=provider
     )
    st.markdown("#### Tasks recomendar criada.")
    st.markdown("#### Objetivo: " + str(guia_turistico.goal))
    return recomendar

# Teste informando o valor da variavel checar_url

def criar_task_url_checker(url_checker_agent):
    url_checker_task = Task(
        description=(
             "Não usar valores de buscas anteriores."
             "Variavel checar_url igual a {checar_url}"
             "Se variavel checar_url for igual a 'Sim', usar a ferramenta de checagem de url, url_checker_tool para verificar se o site esta respodendo com codigo 200 ou não."
             "Se variavel checar_url for igual a 'Não', não executar checagem da url."
             "Checar apenas e somente as melhores classificadas."
             "Variável checar_url igual a {checar_url}."
             "Se variavel checar_url igual a Sim, checar o link da resposta responde com codigo 200."
             "Se variavel checar_url igual a Não, não checar o link."
             "Incluir na resposta final mesmo que nao tenha sido checado."
             "A resposta final deve ter apenas as urls onde a verificação retornou 'True'") ,
        expected_output=
             "Lista com links  dos lugares encontrados. incluir a url para do link. Incluir na resposta um pequeno comentário de cada local."
         ,
         agent=url_checker_agent,
         inputs=['url'],
         outputs=['status_message']
     )
    st.markdown("#### Tasks url_checker_task criada.")
    st.markdown("#### Objetivo: " + str(url_checker_agent.goal))
    return url_checker_task
