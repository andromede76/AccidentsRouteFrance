# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 21:25:24 2024

@author: lebri
"""

import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import seaborn as sns
from xplotter.insights import *
import matplotlib.pyplot as plt


from utils import load_data

st.set_page_config(layout="wide", page_icon="🚗", page_title="Répartition Victimes")

def affichage_annee_filtres(df):
    year_list = list(df['an'].unique())
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox('Année', year_list, 0)
    return year

def pave(df,annee,couleur,type=0):
    
    df = df[(df['an'] == annee)] 
      
    
    categorie = ['gravité', 'sexe','annee naissance','trajet','catégorie']
    
    dico = {
        'grav': 'gravité',
        'sexe': 'sexe',
        'an_nais': 'annee naissance',
        'trajet': 'trajet',
        'catu': 'catégorie'
        
        }
    
    df.rename(columns=dico, inplace=True)
    
    dico_gravite = {1:"Indemne",
            2:"Tué",
            3:"Blessé hospitalisé",
            4:"Blessé léger"}
    
    df['gravité'] = df['gravité'].map(dico_gravite)
    
    
    dico_categorie = {1:"Conducteur",
            2:"Passager",
            3:"Piéton"}
    
    df['catégorie'] = df['catégorie'].map(dico_categorie)
    
   
    dico_sexe  = {1:"Masculin",
            2:"Féminin"}
    
    df['sexe'] = df['sexe'].map(dico_sexe)
       
    
    dico_trajet = {-1:"Non renseigné",
               0:"Non renseigné",
               1:"Domicile travail",
               2:"Domicile ecole",
               3:"Courses achats",
               4:"Utilisation professionnelle",
               5:"Promenade loisirs",
               9:"Autre"}
    
    df['trajet'] = df['trajet'].map(dico_trajet)
    
    usagers=df[categorie].dropna()
    
    
    fig, ax = plt.subplots(figsize=(16, 6))
    
    
    plot_countplot(df=usagers,
               col='sexe',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("sexe",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    usagers_homme = usagers[usagers.sexe == 'Masculin']
    usagers_femme = usagers[usagers.sexe == 'Féminin']
  
    
    # Gravité hommes 
    if (type == 0):
    
        fig, ax = plt.subplots(figsize=(10, 6))
        
        
        
        plot_countplot(df=usagers_homme,
                   col='gravité',
                   order=True,
                   palette=[couleur],
                   ax=ax, orient='h',
                   size_labels=10)
        
        plt.title("Gravité hommes",
              loc="center", fontsize=10, fontstyle='italic')
        
        st.pyplot(fig)
        
        # Gravité femmes 
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        
        plot_countplot(df=usagers_femme,
                   col='gravité',
                   order=True,
                   palette=[couleur],
                   ax=ax, orient='h',
                   size_labels=10)
        
        plt.title("Gravité femmes",
              loc="center", fontsize=10, fontstyle='italic')
        
        st.pyplot(fig)
    
    # trajet hommes 
        
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    plot_countplot(df=usagers_homme,
               col='trajet',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("trajet hommes",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    # trajet femmes 
    
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    plot_countplot(df=usagers_femme,
               col='trajet',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("trajet femmes",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    # catégorie hommes 
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    plot_countplot(df=usagers_homme,
               col='catégorie',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("Catégorie hommes",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    # catégorie femmes 
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    plot_countplot(df=usagers_femme,
               col='catégorie',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("Catégorie femmes",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    
    


def Affichage():
    
    # Chargement des données
    df = pd.read_csv('data/data_Accidents_lieux_usagers_76.csv')
    
    annee = affichage_annee_filtres(df)
    selection = st.selectbox("Selection", ["Accident","Blessures legéres", "Blessés hospitalisés","Tués"])
    
    if selection:
        if selection == "Accident":
            couleur = '#b0cadc'
            
            categorie = ['an','grav', 'sexe','an_nais','trajet','catu']

            df_accident = df[['an','grav', 'sexe','an_nais','trajet','catu']]
            df_accident = df_accident.drop_duplicates()
                                  
            #st.dataframe(df_accident)
                   
            pave(df_accident,annee,couleur)
            
        elif selection == "Blessures legéres":
            couleur = '#f5b005'
            df_bl = df[df.grav == 4]
            pave(df_bl,annee,couleur,4)
            
        elif selection == "Blessés hospitalisés":
            couleur = '#f58405'
            df_bh = df[df.grav ==3]
            pave(df_bh,annee,couleur,3)
            
        elif selection == "Tués":
            couleur = '#f50514'
            df_t = df[df.grav ==2]
            pave(df_t,annee,couleur,2)
    
   #st.dataframe(df)
    
    
    
    
Affichage()