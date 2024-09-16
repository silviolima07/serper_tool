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
             "Variavel checar_url igual a {checar_url}"
             "Numa escala de 0 a 10, onde 0 é a menor importância e 10 a maior importância."
             "Critérios de classificação: beleza natural e a infraestrutura turística entre os turistas."             
             "Classificar os destinos {destino} importância numa escala 8 de importância."
             "Apresentar os critérios usados na classificação final."
             "Faça comentários de cada local recomendando os melhores meses para visitar."
             "Faça sempre em Português do Brasil (pt-br)."
             "O tamanho da lista de recomendações deve ser igual a {n_results}."
             "Incluir na resposta final as urls das recomendaç~eos apresentadas."
             "Apresentar sempre na resposta final uma lista que deve  estar em Português do Brasil (pt-br)."
             ) ,
        expected_output=
             "Lista dos lugares encontrados com comentários a respeito de cada local." # Não incluir a url do link da página do site se variavel checar_url for igual a 'Não'."
         ,
         agent=guia_turistico,
         output_file='lista_resultado',
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