# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 14:59:02 2024

@author: lebri
"""

# Import librairies 
import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium

from utils import chargement_donnees, alignement


APP_TITLE = 'Accidents Seine Maritime'
APP_SUB_TITLE = 'Source: Open Data Gouv'

def affichage_annee_filtres(df):
    year_list = list(df['an'].unique())
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox('Année', year_list, 0)
    return year


def main():
    st.set_page_config(layout="wide",page_icon=":fire_engine:",page_title=APP_TITLE)
    
    df_Accidents_Usagers_76 = pd.read_csv('data/df_Accidents_Usagers_France_76_v1.csv',low_memory=False)
    
    annee = affichage_annee_filtres(df_Accidents_Usagers_76)

    
    st.title(":red_car: Analyse des accidents de la route en Seine Maritime en " + str(annee))
       
    
    df_Accidents_Usagers_76_an = df_Accidents_Usagers_76[df_Accidents_Usagers_76.an == annee]
    
    # Nombre total d'accidents en seine matitime pour l'année sélectionnée
    total_accidents = len(df_Accidents_Usagers_76_an["Num_Acc"].unique())
    total_morts = len(df_Accidents_Usagers_76_an[df_Accidents_Usagers_76_an["grav"] == 2]["Num_Acc"].unique())
    total_blesses_hospitalises = len(df_Accidents_Usagers_76_an[(df_Accidents_Usagers_76_an["grav"] == 3)]["Num_Acc"].unique())
    total_blesses_legers = len(df_Accidents_Usagers_76_an[(df_Accidents_Usagers_76_an["grav"] == 4)]["Num_Acc"].unique())
    
    st.markdown(
        f"""
    <div style="display: inline-block;border: 5px solid blue;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des Accidents: <span style="color: blue; font-weight: bold;">{total_accidents}</span></h2></div>
    <div style="display: inline-block;border: 5px solid red;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des morts:<span style="color: red; font-weight: bold;">{total_morts}</span></h2></div>
    <div style="display: inline-block;border: 5px solid orange;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des blessés hospitalisés:<span style="color: orange; font-weight: bold;">{total_blesses_hospitalises}</span></h2></div>
    <div style="display: inline-block;border: 5px solid yellow;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des blessés légers:<span style="color: yellow; font-weight: bold;">{total_blesses_legers}</span></h2></div>
    """,
        unsafe_allow_html=True,
    )
 
    alignement(3)

    st.write(
    """
    <div style="max-width: 800px;">

    ## Contexte

    ##### Des milliers d'accidents se produisent chaque année en France. Le but de ce projet c'est à partir des données publiques recensant les données détaillées 

    ##### des accidents depuis 2005 d'essayer de comprendre les causes et raisons des accidents.
    
    ##### C'est une première version sur le sujet, les facteurs multiples seront traités ultérieurement. 
    
    ##### Mais déjà il est possible à partir des différents graphiques présentés ici de constater principalement des problèmes comportementaux dans les causes des accidents.
        

   
    </div>
    """,
        unsafe_allow_html=True,
    )
   



if __name__ == "__main__":
    main()
    
    