# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 21:25:24 2024

@author: lebri
"""

import streamlit as st
from utils import load_data
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(layout="wide", page_icon="🚗", page_title="Chiffres nationaux")

def display_graphe(df):
    # Nombre d'accidents par an
    
    fig, ax1 = plt.subplots()

    fig.set_figheight(5)    
    fig.set_figwidth(20)

    ax1.set_ylabel("Nombre d'accidents")
    ax1.set_xlabel("Année")

    ax1.bar(df.an, df.Count, data=df, color="#8891a1",label="Nombre d'accidents en France par année")
  
    plt.xlim(2005, 2023)
    plt.legend()
    st.pyplot(fig)
    
    
    st.markdown("### Chiffres")
    st.dataframe(df)
    

def display_graphe_old(df):
    # Nombre d'accidents par an
    df_count_par_accident=pd.DataFrame({'Count': df["an"].value_counts().sort_index(ascending=True)})
   
    
    label=list(df_count_par_accident.index)
    fig=plt.figure(figsize=[12,5])
    fig.patch.set_facecolor('#E0E0E0')
    fig.patch.set_alpha(0.7)
    plt.title("Nombre d'accidents par année",size=16)
    plt.bar(range(0,len(label)),df_count_par_accident["Count"]
           ,edgecolor='black',color="#8891a1")
    plt.xticks(range(0,len(label)),label,rotation=90,size=13)
    plt.ylabel("Nombre")
    plt.grid()
    
    st.pyplot(fig)
    
    st.markdown("### Chiffres")
    st.dataframe(df)
    
def Accidents_Usagers_Tues_France(df):
    
    fig, ax1 = plt.subplots()

    fig.set_figheight(5)    
    fig.set_figwidth(20)

    ax1.set_ylabel("Nombre de morts")
    ax1.set_xlabel("Année")
    ax1.plot(df.an,df.Count, "red",label='Nombre de tués en France')
  
    plt.xlim(2005, 2023)
    plt.legend()
    st.pyplot(fig)
    
    st.markdown("### Chiffres")
    st.dataframe(df)
    
def Accidents_Usagers_Blesses_France(df):
    
    fig, ax1 = plt.subplots()

    fig.set_figheight(5)    
    fig.set_figwidth(20)

    ax1.set_ylabel("Nombre de Blessés")
    ax1.set_xlabel("Année")
   
    ax1.plot(df.an, df.Count, "blue",label='Nombre de blessés hospitalisés en France')

    plt.xlim(2005, 2023)
    plt.legend()
    st.pyplot(fig)
    
    st.markdown("### Chiffres")
    st.dataframe(df)
    
    
    
def Accidents_Usagers_Tues_France_old(df):
    
    # Dataset des personnes tuées en France
    df_Tues = df[df.grav == 2 ]
    df_count_Tues=pd.DataFrame({'Count': df_Tues["an"].value_counts().sort_index(ascending=True)})
    
    fig, ax1 = plt.subplots()

    fig.set_figheight(5)    
    fig.set_figwidth(20)

    ax1.set_ylabel("Nombre de morts")
    ax1.set_xlabel("Année")
    ax1.plot(df_count_Tues, "red",label='Nombre de tués en France')
  
    plt.xlim(2005, 2023)
    plt.legend()
    st.pyplot(fig)
    
    
def Accidents_Usagers_Blesses_France_old(df):
    
            
    df_Blesses = df[(df.grav == 3) & (df.grav == 3)]
    df_count_Blesses=pd.DataFrame({'Count': df_Blesses["an"].value_counts().sort_index(ascending=True)})
        
    
    fig, ax1 = plt.subplots()

    fig.set_figheight(5)    
    fig.set_figwidth(20)

    ax1.set_ylabel("Nombre de Blessés")
    ax1.set_xlabel("Année")
   
    ax1.plot(df_count_Blesses, "blue",label='Nombre de blessés hospitalisés en France')

    plt.xlim(2005, 2023)
    plt.legend()
    st.pyplot(fig)
    
# Nombre d'accidents par année et région
def Accidents_Par_Region_Et_Annee(df, annee):   
    
    count_accident_par_region_et_annee = df[df.an == annee]
    
    df_count=pd.DataFrame({'Count': count_accident_par_region_et_annee["regionName"].value_counts().sort_values(ascending = False)})   
     
    label=list(df_count.index)
    fig=plt.figure(figsize=[12,5])
    fig.patch.set_facecolor('#E0E0E0')
    fig.patch.set_alpha(0.7)
    plt.title("Nombre d'accidents par régions",size=16)
    plt.bar(range(0,len(label)),df_count["Count"]
           ,edgecolor='black',color="#8891a1")
    plt.xticks(range(0,len(label)),label,rotation=90,size=13)
    plt.ylabel("Nombre")
    plt.grid()
    st.pyplot(fig)
    
    st.markdown("### Chiffres")
    st.dataframe(df_count)
    
# Nombre usagers gravites par année et région
def Accidents_Individus_Par_Region_Et_Annee(df, annee,grav,titre):   
    
    count_par_region_et_annee = df[(df.an == annee) & (df.grav == grav)]
    
    df_count=pd.DataFrame({'Count': count_par_region_et_annee["regionName"].value_counts().sort_values(ascending = False)})   
     
    label=list(df_count.index)
    fig=plt.figure(figsize=[12,5])
    fig.patch.set_facecolor('#E0E0E0')
    fig.patch.set_alpha(0.7)
    plt.title(titre,size=16)
    plt.bar(range(0,len(label)),df_count["Count"]
           ,edgecolor='black',color="#8891a1")
    plt.xticks(range(0,len(label)),label,rotation=90,size=13)
    plt.ylabel("Nombre")
    plt.grid()
    st.pyplot(fig)
    
    st.markdown("### Chiffres")
    st.dataframe(df_count)
    
    
# Nombre d'accidents par année et région
def Accidents_Par_Region_Et_Annee_old(df):
              
    
    dfp = df.pivot_table(index='an', columns='regionName', values='Num_Acc', aggfunc='count')  
    
    fig, ax1 = plt.subplots()
    
    fig.set_figheight(5)    
    fig.set_figwidth(20)
    
    ax1.set_ylabel("Nombre de Blessés")
    ax1.set_xlabel("Année")
        
    #ax1.plot(dfp,"blue",label="Nombre de blessés")
    ax1.plot(dfp,label=dfp.columns)
    ax1.legend(bbox_to_anchor=(1, 1.02), loc='upper left')
    
    plt.xlim(2005, 2023)
    plt.legend()
    st.pyplot(fig)
  
  
    st.dataframe(dfp)
    
def affichage_annee_filtres(df):
    year_list = list(df['an'].unique())
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox('Année', year_list, 0)
    return year

def Affichage():
        
    
    st.title(f" Chiffres des accidents en France")
        
   
    # Chargement des données
    #df_accidents_France = pd.read_csv('data/Accidents_France_2005_to_2023.csv',low_memory=False)
    #df_Accidents_Usagers_France = pd.read_csv('data/fusion_usagers_France_2005_to_2023.csv',low_memory=False)
    
    df_accidents_France = pd.read_csv('data/df_Accidents_light.csv',low_memory=False)
    #df_Accidents_Usagers_France = pd.read_csv('data/df_Usagers_light.csv',low_memory=False)
    
    df_Accidents_Usagers_France_tues_V1 = pd.read_csv('data/df_Accidents_Usagers_France_tues_V1.csv',low_memory=False)
    df_Accidents_Usagers_France_Blesses_hospitalises = pd.read_csv('data/df_Accidents_Usagers_France_Blesses_hospitalises.csv',low_memory=False)
    df_Accidents_Usagers_France_Blesses_legers = pd.read_csv('data/df_Accidents_Usagers_France_Blesses_legers.csv',low_memory=False)
    
 
    
    df_count_par_accident = pd.read_csv('data/dfResult_group_accident.csv')
    df_count_Usagers_Tues_Group = pd.read_csv('data/df_count_Usagers_Tues_Group.csv')
    df_count_Usagers_Blesses_Group = pd.read_csv('data/df_count_Usagers_Blesses_Group.csv')
   
           
    display_graphe(df_count_par_accident)    
    #display_graphe(df_accidents_France)    
        
    
    #st.markdown("### Nombre de tués")
    Accidents_Usagers_Tues_France(df_count_Usagers_Tues_Group)
    #st.markdown("### Nombre de blessés")
    Accidents_Usagers_Blesses_France(df_count_Usagers_Blesses_Group)

    
    annee = affichage_annee_filtres(df_count_par_accident)
    
    Accidents_Par_Region_Et_Annee(df_accidents_France,annee)
    st.markdown("### Nombre de tués")
    
    
    
    Accidents_Individus_Par_Region_Et_Annee(df_Accidents_Usagers_France_tues_V1, annee,2,"Nombre de tués par région et année")
    st.markdown("### Nombre de blessés hospitalisés")
    Accidents_Individus_Par_Region_Et_Annee(df_Accidents_Usagers_France_Blesses_hospitalises, annee,3,"Nombre de blessés hospitalisés par régions et année")
    st.markdown("### Nombre de blessés légers")
    Accidents_Individus_Par_Region_Et_Annee(df_Accidents_Usagers_France_Blesses_legers, annee,4,"Nombre de blessés legers par régions et année")
 

Affichage()