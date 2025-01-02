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
    
    df_a = df[df.an > 2018]
    
    year_list = list(df_a['an'].unique())
    
     
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox('Année', year_list, 0)
    return year
    
    #year_list = list(df['an'].unique())
    #year_list.sort(reverse=True)
    #year = st.sidebar.selectbox('Année', year_list, 0)
    #return year


def main():
    st.set_page_config(layout="wide",page_icon=":fire_engine:",page_title=APP_TITLE)
    
    df_Accidents_Usagers_76 = pd.read_csv('data/df_Accidents_Usagers_France_76_v1.csv',low_memory=False)
    df_Usagers_76 = pd.read_csv('data/data_Accidents_lieux_usagers_76.csv')
       
    annee = affichage_annee_filtres(df_Accidents_Usagers_76)

    
    st.title(":red_car: Analyse des accidents de la route en Seine Maritime en " + str(annee))
       
    
    df_Accidents_Usagers_76_an = df_Accidents_Usagers_76[df_Accidents_Usagers_76.an == annee]
    df_Usagers_76_an = df_Usagers_76[df_Usagers_76.an == annee]
        
    
    # Nombre total d'accidents en seine matitime pour l'année sélectionnée
    total_accidents = len(df_Accidents_Usagers_76_an["Num_Acc"].unique())
    total_morts = len(df_Accidents_Usagers_76_an[df_Accidents_Usagers_76_an["grav"] == 2]["Num_Acc"].unique())
    total_blesses_hospitalises = len(df_Accidents_Usagers_76_an[(df_Accidents_Usagers_76_an["grav"] == 3)]["Num_Acc"].unique())
    total_blesses_legers = len(df_Accidents_Usagers_76_an[(df_Accidents_Usagers_76_an["grav"] == 4)]["Num_Acc"].unique())
    
    # Nombre d'accidents Hommes 
    df_Usagers_76_an_hommes = df_Usagers_76_an[df_Usagers_76_an.sexe == 1]
    
    total_accidents_hommes = len(df_Usagers_76_an_hommes["Num_Acc"].unique())
    
    total_accidents_hommes_decedes = df_Usagers_76_an[df_Usagers_76_an.grav == 2].shape[0]
          
    total_accidents_hommes_blesses_hospitalises = df_Usagers_76_an[df_Usagers_76_an.grav == 3].shape[0]
    total_accidents_hommes_blesses_legers = df_Usagers_76_an[df_Usagers_76_an.grav == 4].shape[0]
            
    
    df_Usagers_76_an_femmes = df_Usagers_76_an[df_Usagers_76_an.sexe == 2]
    total_accidents_femmes = len(df_Usagers_76_an_femmes["Num_Acc"].unique())
        
    total_accidents_femmes_decedes = df_Usagers_76_an_femmes[df_Usagers_76_an_femmes.grav == 2].shape[0]
    total_accidents_femmes_blesses_hospitalises = df_Usagers_76_an_femmes[df_Usagers_76_an_femmes.grav == 3].shape[0]
    total_accidents_femmes_blesses_legers = df_Usagers_76_an_femmes[df_Usagers_76_an_femmes.grav == 4].shape[0]
    
    
    st.markdown(
        f"""
    <div style="display: inline-block;border: 5px solid blue;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des Accidents: <span style="color: blue; font-weight: bold;">{total_accidents}</span></h2></div>
    <div style="display: inline-block;border: 5px solid red;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des morts:<span style="color: red; font-weight: bold;">{total_morts}</span></h2></div>
    <div style="display: inline-block;border: 5px solid orange;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des blessés hospitalisés:<span style="color: orange; font-weight: bold;">{total_blesses_hospitalises}</span></h2></div>
    <div style="display: inline-block;border: 5px solid yellow;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des blessés légers:<span style="color: yellow; font-weight: bold;">{total_blesses_legers}</span></h2></div>
    
    
    <div style="display: inline-block;border: 5px solid blue;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des Accidents hommes: <span style="color: blue; font-weight: bold;">{total_accidents_hommes}</span></h2></div>
    <div style="display: inline-block;border: 5px solid red;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des morts hommes :<span style="color: red; font-weight: bold;">{total_accidents_hommes_decedes}</span></h2></div>
    <div style="display: inline-block;border: 5px solid orange;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des blessés hospitalisés hommes:<span style="color: orange; font-weight: bold;">{total_accidents_hommes_blesses_hospitalises}</span></h2></div>
    <div style="display: inline-block;border: 5px solid yellow;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des blessés légers hommes :<span style="color: yellow; font-weight: bold;">{total_accidents_hommes_blesses_legers}</span></h2></div>
    
    <div style="display: inline-block;border: 5px solid blue;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des Accidents femmes: <span style="color: blue; font-weight: bold;">{total_accidents_femmes}</span></h2></div>
    <div style="display: inline-block;border: 5px solid red;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des morts femmes :<span style="color: red; font-weight: bold;">{total_accidents_femmes_decedes}</span></h2></div>
    <div style="display: inline-block;border: 5px solid orange;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des blessés hospitalisés femmes:<span style="color: orange; font-weight: bold;">{total_accidents_femmes_blesses_hospitalises}</span></h2></div>
    <div style="display: inline-block;border: 5px solid yellow;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total des blessés légers femmes :<span style="color: yellow; font-weight: bold;">{total_accidents_femmes_blesses_legers}</span></h2></div>
    
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
    
    ##### A première vue l'on voit qu'il y a principalement un problème de comportement indépendamment des autres causes. 
    
    ##### Les hommes sont beaucoup plus dangereux que les femmes. Les femmes et les hommes ont une égalisé de circulation mais une forte inégalité dans l'accidentologie.
  
   
    </div>
    """,
        unsafe_allow_html=True,
    )
   



if __name__ == "__main__":
    main()
    
    