# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 21:25:24 2024

@author: lebri
"""

import streamlit as st
from utils import chargement_donnees
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_icon="🚗", page_title="Chiffres Seine Maritime")

def display_graphe(df,titre):
    # Nombre d'accidents par année en Seine maritime
    df_count_par_accident=pd.DataFrame({'Count': df["an"].value_counts().sort_index(ascending=True)})
    
    label=list(df_count_par_accident.index)
    fig=plt.figure(figsize=[12,5])
    fig.patch.set_facecolor('#E0E0E0')
    fig.patch.set_alpha(0.7)
    plt.title(titre,size=16)
    plt.bar(range(0,len(label)),df_count_par_accident["Count"]
           ,edgecolor='black',color="#8891a1")
    plt.xticks(range(0,len(label)),label,rotation=90,size=13)
    plt.ylabel("Nombre")
    plt.grid()
    
    st.pyplot(fig)
    
    st.markdown("### Chiffres")
    st.dataframe(df_count_par_accident)

def affichage_annee_filtres(df):
    year_list = list(df['an'].unique())
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox('Année', year_list, 0)
    return year


def Affichage():
    
   #st.title(f" Chiffres des accidents en Seine Maritime")
    
    # Chargement des données
    
    #df_accidents_76 = pd.read_csv('data/df_SeineMaritime_Accidents_2005_2023.csv')
    #df_Accidents_Usagers_France = pd.read_csv('data/fusion_usagers_France_2005_to_2023.csv',low_memory=False) 
    
    df_accidents_76 = pd.read_csv('data/df_accidents_France_76_v1.csv',low_memory=False)
    df_Accidents_Usagers_France = pd.read_csv('data/df_Accidents_Usagers_France_76_v1.csv',low_memory=False)
      
    
    #df_accidents_76 = df_accidents_France[df_accidents_France.dep == 76]
        
    df_Accidents_Usagers_76 = df_Accidents_Usagers_France[df_Accidents_Usagers_France.dep == 76]
    
    #Personnes tués
    Accidents_2005_to_2023_tues_76 = df_Accidents_Usagers_76[(df_Accidents_Usagers_76["grav"]==2)]
    # Personnes blessés hospitalisés
    Accidents_2005_to_2023_Blesses_hospitalises_departement_76 = df_Accidents_Usagers_76[(df_Accidents_Usagers_76["grav"]==3)]
    # Personnes blessés legers
    Accidents_2005_to_2023_Blesses_legers_departement_76 = df_Accidents_Usagers_76[(df_Accidents_Usagers_76["grav"]==4)]
    
    annee = affichage_annee_filtres(df_accidents_76)
    
    st.title(":red_car: Chiffres des accidents en Seine Maritime pour l'année " + str(annee))
    
    display_graphe(df_accidents_76,"Nombre d'accidents en Seine Maritime par années")
    display_graphe(Accidents_2005_to_2023_tues_76,"Nombre de tués en Seine Maritime par années")
    display_graphe(Accidents_2005_to_2023_Blesses_hospitalises_departement_76,"Nombre de blessés hospitalisés en Seine Maritime par années")
    display_graphe(Accidents_2005_to_2023_Blesses_legers_departement_76,"Nombre de blessés legers en Seine Maritime par années")

Affichage()