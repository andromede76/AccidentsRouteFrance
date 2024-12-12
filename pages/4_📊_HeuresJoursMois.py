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

st.set_page_config(layout="wide", page_icon="🚗", page_title="Heures Jours Mois")

def affichage_annee_filtres(df):
    year_list = list(df['an'].unique())
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox('Année', year_list, 0)
    return year

# Construction des tranches horaires de la journée
def affichage_tranches_horaires(df,annee,couleur,titre):
        

    df = df[(df['an'] == annee)] 
    df['tranche_heure'] = pd.cut(df.heure,
                                            bins=[-1,5,7,9,11,14,16,18,20,23],
                                            labels=['0h-4h', # nuit
                                                    '5h-7h', # nuit 
                                                    '8h_9h',     # matin
                                                    '10h-11h',   # matinée
                                                    '12h-14h',   # midi 
                                                    '15h-16h',   # après_midi
                                                    '17h-18h',   # début de soirée 
                                                    '19h_20h',   # diner
                                                    '20h-23h'])  # soirée

    df['tranche_heure'].value_counts(sort=False)
    
    fig, ax = plt.subplots(figsize=(6,4))

    plot_countplot(df=df, 
               col='tranche_heure', 
               order=False,
               palette=[couleur],
               ax=ax, orient='h', 
               size_labels=8)

    plt.title(titre, loc="center", fontsize=10, fontstyle='italic')
    st.pyplot(fig)
    
def affichage_mois(df,annee,couleur,titre):
    
    df = df[(df['an'] == annee)] 
    
    dico = {1 : 'janvier',
               2 : 'fevrier',
               3 : 'mars',
               4 : 'avril',
               5 : 'mai',
               6 : 'juin',
               7 : 'juillet',
               8 : 'aout',
               9 : 'septembre',
               10 : 'octobre',
               11 : 'novembre',
               12 : 'decembre'
               
               }
    
    df['mois'] = df['mois'].map(dico)
    
    
    #st.dataframe(df)
        
    fig, ax = plt.subplots(figsize=(6,4))

    plot_countplot(df=df, 
                   col='mois', 
                   order=True,
                   palette=[couleur],
                   ax=ax, orient='h', 
                   size_labels=8)

    plt.title(titre, loc="center", fontsize=10, fontstyle='italic')
    st.pyplot(fig)
    

def affichage_jours_semaine(df,annee,couleur,titre):
    
    df = df[(df['an'] == annee)] 
    
    df['semaine'] = df['date'].dt.weekday

    dico = {0 : 'Lundi',
               1 : 'Mardi',
               2 : 'Mercredi',
               3 : 'Jeudi',
               4 : 'Vendredi',
               5 : 'Samedi',
               6 : 'Dimanche'}

    df['semaine'] = df['semaine'].map(dico)

    fig, ax = plt.subplots(figsize=(6,4))

    plot_countplot(df=df, 
                   col='semaine', 
                   order=True,
                   palette=[couleur],
                   ax=ax, orient='h', 
                   size_labels=8)

    plt.title(titre, loc="center", fontsize=10, fontstyle='italic')
    st.pyplot(fig)
    

def Affichage():
    
    # Chargement des données
    df_accidents_lieux_usagers_76 = pd.read_csv('data/data_Accidents_lieux_usagers_76.csv')
    df_accidents_76 = pd.read_csv('data/df_SeineMaritime_Accidents_2005_2023.csv')
    
    # Création d'une date exploitable

    df_accidents_lieux_usagers_76['date'] = df_accidents_lieux_usagers_76['jour'].astype(str) + '-' + df_accidents_lieux_usagers_76['mois'].astype(str) + '-' + df_accidents_lieux_usagers_76['an'].astype(str)
    df_accidents_lieux_usagers_76['date'] = pd.to_datetime(df_accidents_lieux_usagers_76['date'])
    
    df_accidents_lieux_usagers_76['hrmn'] = df_accidents_lieux_usagers_76['hrmn'].str.replace(':', '')
    df_accidents_lieux_usagers_76['heure'] = df_accidents_lieux_usagers_76['hrmn'].astype(int)//100
    
    
    annee = affichage_annee_filtres(df_accidents_76)
    selection = st.selectbox("Selection", ["Accident","Blessures legéres", "Blessés hospitalisés","Tués"])
    
    if selection:
        if selection == "Accident":
            couleur = '#b0cadc'
            
            #st.dataframe(df_accidents_lieux_usagers_76)
                        

            df_accident = df_accidents_lieux_usagers_76[['date','an','Num_Acc']]
            df_accident = df_accident.drop_duplicates()
                      
            affichage_jours_semaine(df_accident,annee,couleur,"Nombre d'accidents selon le jour la semaine\n")
            
            df_accident_horaire = df_accidents_lieux_usagers_76[['heure','an','Num_Acc']]
            df_accident_horaire = df_accident_horaire.drop_duplicates()
            
            affichage_tranches_horaires(df_accident_horaire,annee,couleur,"Nombre d'accidents selon la tranche horaire de la journée\n")
            
            df_accident_mois = df_accidents_lieux_usagers_76[['mois','an','Num_Acc']]
            df_accident_mois = df_accident_mois.drop_duplicates()
            
            affichage_mois(df_accident_mois,annee,couleur,"Nombre d'accidents par mois\n")
                            
                
        ###       
        elif selection == "Blessures legéres":
            couleur = '#f5b005'
                        
            df_accident = df_accidents_lieux_usagers_76[['date','an','grav']]
            df_accident_bl = df_accident[df_accident.grav == 4]
            
            affichage_jours_semaine(df_accident_bl,annee,couleur,"Nombre de blessés legers selon le jour la semaine\n")
            
            df_accident_horaire = df_accidents_lieux_usagers_76[['heure','an','Num_Acc','grav']]
            df_accident_horaire = df_accident_horaire.drop_duplicates()
            
            df_accident_horaire_bl = df_accident_horaire[df_accident_horaire.grav == 4]
            
            affichage_tranches_horaires(df_accident_horaire_bl,annee,couleur,"Nombre de blessés legers selon la tranche horaire de la journée\n")
            
            df_accident_mois = df_accidents_lieux_usagers_76[['mois','an','Num_Acc','grav']]
            df_accident_mois_bl = df_accident_mois[df_accident_mois.grav == 4]
            df_accident_mois_bl = df_accident_mois_bl.drop_duplicates()
            
            affichage_mois(df_accident_mois_bl,annee,couleur,"Nombre de blesses legers par mois\n")
                        
        elif selection == "Blessés hospitalisés":
            couleur = '#f58405'
            
            df_accident = df_accidents_lieux_usagers_76[['date','an','grav']]
            df_accident_bh = df_accident[df_accident.grav == 3]
            
            affichage_jours_semaine(df_accident_bh,annee,couleur,"Nombre de blessés hospitalisés selon le jour la semaine\n")
            
            df_accident_horaire = df_accidents_lieux_usagers_76[['heure','an','Num_Acc','grav']]
            df_accident_horaire = df_accident_horaire.drop_duplicates()
            
            df_accident_horaire_bh = df_accident_horaire[df_accident_horaire.grav == 3]
            
            affichage_tranches_horaires(df_accident_horaire_bh,annee,couleur,"Nombre de blessés hospitalisés selon la tranche horaire de la journée\n")
            
            df_accident_mois = df_accidents_lieux_usagers_76[['mois','an','Num_Acc','grav']]
            df_accident_mois_bh = df_accident_mois[df_accident_mois.grav == 3]
            df_accident_mois_bh = df_accident_mois_bh.drop_duplicates()
            
            affichage_mois(df_accident_mois_bh,annee,couleur,"Nombre de blesses hospitalisés par mois\n")
            
        elif selection == "Tués":
            couleur = '#f50514'
            
            df_accident = df_accidents_lieux_usagers_76[['date','an','grav']]
            df_accident_t = df_accident[df_accident.grav == 2]
            
            affichage_jours_semaine(df_accident_t,annee,couleur,"Nombre de tués selon le jour la semaine\n")
            
            df_accident_horaire = df_accidents_lieux_usagers_76[['heure','an','Num_Acc','grav']]
            df_accident_horaire = df_accident_horaire.drop_duplicates()
            
            df_accident_horaire_t = df_accident_horaire[df_accident_horaire.grav == 2]
            
            affichage_tranches_horaires(df_accident_horaire_t,annee,couleur,"Nombre de tués selon la tranche horaire de la journée\n")
            
            df_accident_mois = df_accidents_lieux_usagers_76[['mois','an','Num_Acc','grav']]
            df_accident_mois_t = df_accident_mois[df_accident_mois.grav == 2]
            df_accident_mois_t = df_accident_mois_t.drop_duplicates()
            
            affichage_mois(df_accident_mois_t,annee,couleur,"Nombre de tués par mois\n")
            
   
        ###
    
   #st.dataframe(df)
    
    
    
    
Affichage()