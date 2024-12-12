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

APP_TITLE = 'Accidents Seine Maritime'
APP_SUB_TITLE = 'Source: Open Data Gouv'


def main():
    st.set_page_config(layout="wide",page_icon=":fire_engine:",page_title=APP_TITLE)

    
    st.title(":red_car: Analyse des accidents de la route en Seine Maritime.")
   

 
    # Nombre de tués
    # Nombre de blessés hospitalisés
    # Nombre de blésses légers
    
   
   
    
    #annee = affichage_annee_filtres(df_accidents_76)
    #display_map(df_accidents_76, annee)


if __name__ == "__main__":
    main()
    
    