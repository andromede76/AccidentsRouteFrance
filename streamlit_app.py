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
    #total_morts = len(df_Accidents_Usagers_76_an[df_Accidents_Usagers_76_an["grav"] == 2]["Num_Acc"].unique())
    #total_blesses_hospitalises = len(df_Accidents_Usagers_76_an[(df_Accidents_Usagers_76_an["grav"] == 3)]["Num_Acc"].unique())
    #total_blesses_legers = len(df_Accidents_Usagers_76_an[(df_Accidents_Usagers_76_an["grav"] == 4)]["Num_Acc"].unique())
    
    # Nombre d'accidents Hommes 
    df_Usagers_76_an_hommes = df_Usagers_76_an[df_Usagers_76_an.sexe == 1]
    
    #total_accidents_hommes = len(df_Usagers_76_an_hommes["Num_Acc"].unique())
    
    total_accidents_hommes_decedes = df_Usagers_76_an_hommes[df_Usagers_76_an_hommes.grav == 2].shape[0]
          
    total_accidents_hommes_blesses_hospitalises = df_Usagers_76_an_hommes[df_Usagers_76_an_hommes.grav == 3].shape[0]
    total_accidents_hommes_blesses_legers = df_Usagers_76_an_hommes[df_Usagers_76_an_hommes.grav == 4].shape[0]
            
    
    df_Usagers_76_an_femmes = df_Usagers_76_an[df_Usagers_76_an.sexe == 2]
    #total_accidents_femmes = len(df_Usagers_76_an_femmes["Num_Acc"].unique())
        
    total_accidents_femmes_decedes = df_Usagers_76_an_femmes[df_Usagers_76_an_femmes.grav == 2].shape[0]
    total_accidents_femmes_blesses_hospitalises = df_Usagers_76_an_femmes[df_Usagers_76_an_femmes.grav == 3].shape[0]
    total_accidents_femmes_blesses_legers = df_Usagers_76_an_femmes[df_Usagers_76_an_femmes.grav == 4].shape[0]
    
    total_morts = total_accidents_hommes_decedes + total_accidents_femmes_decedes
    total_blesses_hospitalises = total_accidents_hommes_blesses_hospitalises + total_accidents_femmes_blesses_hospitalises
    total_blesses_legers = total_accidents_hommes_blesses_legers + total_accidents_femmes_blesses_legers
    
    
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
    
    # Division de la page en 5 colonnes pour les KPIs
    col1, col2, col3 = st.columns(3)
    
    # Statistiques générales par genre homme 
    with col1:
        st.metric(label="⚰️ Nombre de blessés hommes légers", value=f"{total_accidents_hommes_blesses_legers}")
    with col2:
        st.metric(label="🚘 Nombre de blessés hommes hospitalisés", value=f"{total_accidents_hommes_blesses_hospitalises}")
    with col3:
        st.metric(label="🧍 Nombre de décédés hommes", value=f"{total_accidents_hommes_decedes}")
        
    # Statistiques générales par genre femme 
    with col1:
        st.metric(label="⚰️ Nombre de blessés femmes légers", value=f"{total_accidents_femmes_blesses_legers}")
    with col2:
        st.metric(label="🚘 Nombre de blessés femmes hospitalisés", value=f"{total_accidents_femmes_blesses_hospitalises}")
    with col3:
        st.metric(label="🧍 Nombre de décédés femmes", value=f"{total_accidents_femmes_decedes}")
        
        
    st.subheader("🧾Description:")
    st.text("""Des milliers d'accidents routiers se produisent chaque année en France. 
            Le but de ce projet c'est à partir des données publiques recensant les données détaillés des accidents depuis 2005 
            de comprendre les causes et raisons des accidents. 
            """)
    
    st.markdown("Source des données: [Cliquer ici](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2023/)")

    st.subheader("🧭 Résultats:")
    st.text(""" Ce qui frappe c’est les graphiques par genre.
            En 2023 le pourcentage d’accidents est de 63% pour les hommes et de 37% pour les femmes. 
            Au niveau des décédés toujours en 2023 c’est 90 % de sexe masculin et 10% de femmes.
            Quand on regarde les autres années, on arrive à peu près au même rapport hommes femmes.  
            Le nombre de conducteurs entre hommes et femmes est apparemment sensiblement égales. 
            Donc une égalité dans la circulation mais une forte inégalité dans les accidents, tués et blessés. 
            L’insécurité routière est surtout une affaire de genres 
            """)

    st.markdown("Lien du projet sur Github: [Cliquer ici](https://github.com/andromede76/AccidentsRouteFrance)")                  

   



if __name__ == "__main__":
    main()
    
    