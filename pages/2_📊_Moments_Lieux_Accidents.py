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


from utils import chargement_donnees

st.set_page_config(layout="wide", page_icon="🚗", page_title="Moments et lieux des accidents")

def display_map(df,radars, annee):
    df = df[(df['an'] == annee)]
    
    radars_76 = radars[radars.departement == '76']
    radars_76.rename(columns={'latitude' : 'lat', 'longitude' : 'long'},inplace=True)
    radars_76['an'] = radars_76['date_heure_dernier_changement'].str[:4].astype('int')
    
    radars = radars_76[radars_76.an <= annee]
    
    # Affichage d'une carte centré a partir d'une latitude et longitude
    stations_map = folium.Map(location=[45,1], zoom_start=15)


    def plotDot(point):
        '''input: series that contains a numeric named latitude and a numeric named longitude
        this function creates a CircleMarker and adds it to your this_map'''
        folium.CircleMarker(location=[point.latitude, point.longitude],
                        radius=2,
                        weight=5).add_to(stations_map)
    
    stations_map.add_child(folium.GeoJson('data/departement-76-seine-maritime.geojson'))
    
    colors = ['red','green']

    for index, row in df.iterrows():
        
        folium.CircleMarker(location=[row.lat, row.long],
                        radius=2,
                        weight=5,
                        color = colors[1]
                        ).add_to(stations_map)
        
    for index, row in radars.iterrows():
        
        folium.CircleMarker(location=[row.lat, row.long],
                        radius=2,
                        weight=5,
                        color = colors[0]
                        ).add_to(stations_map) 
        
        
    stations_map.fit_bounds(stations_map.get_bounds())
       
    
    st_map = st_folium(stations_map, width=1300, height=750)
    
def affichage_annee_filtres(df):
    
    df_a = df[df.an > 2018]
    
    year_list = list(df_a['an'].unique())
    
     
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox('Année', year_list, 0)
    return year



def pave_Arrondissement(df,annee,couleur):
    df = df[(df['an'] == annee)] 
    
    categorie = ['Arrondissement']
    
    dico = {1:"Dieppe",
            2:"Le Havre",
            3:"Rouen"}            
    
    df['Arrondissement'] = df['Arrondissement'].map(dico)
    
    accidents=df[categorie].dropna()
    #st.dataframe(accidents)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    plot_countplot(df=accidents,
               col='Arrondissement',
               order=True,
               palette=[couleur],
               ax=ax, orient='v',
               size_labels=10)
    plt.title("Arrondissement",
          loc="center", fontsize=10, fontstyle='italic')
    st.pyplot(fig)
    
    

def pave_usagers(df,annee,couleur):
    df = df[(df['an'] == annee)] 
    
    categorie = ['gravité', 'sexe','annee naissance','trajet','catégorie','place','catu']
    
    dico = {
        'grav': 'gravité',
        'sexe': 'sexe',
        'An_nais': 'annee naissance',
        'trajet': 'trajet',
        'place': 'place',
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
    
    df['catu'] = df['catu'].map(dico_categorie)
    
   
    dico_sexe  = {1:"Masculin",
            2:"Féminin"}
    
    df['sexe'] = df['sexe'].map(dico_sexe)
       
    
    dico_trajet = {-1:"Non renseigné",
               0:"Non renseigné",
               1:"Domicile âtravail",
               2:"Domicile âecole",
               3:"Courses âachats",
               4:"Utilisation professionnelle",
               5:"Promenade loisirs",
               9:"Autre"}
    
    df['trajet'] = df['trajet'].map(dico_trajet)
    
    

def pave_vehicule(df,annee,couleur):
    df = df[(df['an'] == annee)] 
    
    #st.dataframe(df)
    
    categorie = ['Catégorie véhicule', 'Obstacle rencontré','Obstacle mobile rencontré','Point choc initial','Manoeuvre principale']
    
    dico = {
        'catv': 'Catégorie véhicule',
        'obs': 'Obstacle rencontré',
        'obsm': 'Obstacle mobile rencontré',
        'choc': 'Point choc initial',
        'manv': 'Manoeuvre principale'
        
        }
    
    df.rename(columns=dico, inplace=True)
    
     
    dico_categorie = {0:"Indéterminable",
            1:"Bicyclette",
            2:"Cyclomoteur <50cm3",
            3:"Voiturette",
            4:"Scooter",
            5:"motocyclette",
            6:"Side-car",
            7:"VL seul",
            8:"VL + caravane",
            9:"VL + remorque",
            10:"VU",
            11:"VU  + caravane)",
            12:"VU + remorque",
            13:"PL <= 7.5",
            14:"PL >7,5T",
            15:"PL > 3,5T + remorque",
            16:"Tracteur routier seul",
            17:"Tracteur routier + semi-remorque",
            18:"Transport en commun",
            19:"Tramway)",
            20:"Engin spécial",
            21:"Tracteur agricole",
            30:"Scooter < 50 cm3",
            31:"Motocyclette > 50 cm3 et <= 125 cm3",
            32:"Scooter > 50 cm3 et <= 125 cm3",
            33:"Motocyclette > 125 cm3",
            34:"Scooter > 125 cm3",
            35:"Quad léger <= 50 cm3",
            36:"Quad lourd > 50 cm3",
            37:"Autobus",
            38:"Autocar",
            39:"Train",
            40:"Tramway",
            41:"3RM <= 50 cm3",
            42:"3RM > 50 cm3 <= 125 cm3",
            43:"3RM > 125 cm3",
            50:"EDP Ã  moteur",
            60:"EDP sans moteur",
            80:"VAE",
            99:"Autre véhicule"}
    

    df['Catégorie véhicule'] = df['Catégorie véhicule'].map(dico_categorie)
    
    dico_obstacle = {-1:"Non renseigné",
           0:"Sans objet",
           1:"Véhicule en stationnement",
           2:"Arbre",
           3:"Glissière métallique",
           4:"Glissière béton",
           5:"Autre glissière",
           6:"Batiment, mur, pile de pont",
           7:"Support de signalisation",
           8:"Poteau",
           9:"Mobilier urbain",
           10:"Parapet",
           11:"Ilot, refuge, borne haute",
           12:"Bordure de trottoir",
           13:"Fossé, talus, paroi rocheuse",
           14:"Autre obstacle fixe sur chaussée",
           15:"Autre obstacle fixe sur trottoir ou accotement",
           16:"Sortie de chaussée sans obstacle",
           17:"Buse âtête d'aqueduc"}
   
    df['Obstacle rencontré'] = df['Obstacle rencontré'].map(dico_obstacle)
    
    dico_obstacle_mobile = {-1:"Non renseigné",
           0:"Aucun",
           1:"Piéton",
           2:"Véhicule",
           4:"Véhicule sur rail",
           5:"Animal domestique",
           6:"Animal sauvage",
           9:"Autre"}
   
    df['Obstacle mobile rencontré'] = df['Obstacle mobile rencontré'].map(dico_obstacle_mobile)
    
    dico_obstacle = {-1:"Non renseigné",
            0:"Aucun",
            1:"Avant",
            2:"Avant droit",
            3:"Avant gauche",
            4:"Arrière",
            5:"Arrière droit",
            6:"Arrière gauche",
            7:"Coté droit",
            8:"Coté gauche",
            9:"Chocs multiples (tonneaux)"}
    
    df['Point choc initial'] = df['Point choc initial'].map(dico_obstacle)
    
    dico_manoeuvre = {-1:"Non renseigné",
           0:"Inconnue",
           1:"Sans changement de direction",
           2:"Même sens, même file",
           3:"Entre 2 files",
           4:"En marche arrière",
           5:"A contresens",
           6:"En franchissant le terre-plein central",
           7:"Dans le couloir bus, dans le même sens",
           8:"Dans le couloir bus, dans le sens inverse",
           9:"En s'insérant",
           10:"En faisant demi-tour sur la chaussée",
           11:"Changeant de file à  gauche",
           12:"Changeant de file à  droite",
           13:"Déporté à  gauche",
           14:"Déporté à  droite",
           15:"Tournant à  gauche",
           16:"Tournant à  droite",
           17:"Dépassant à  gauche",
           18:"Dépassant à  droite",
           19:"Traversant la chaussée",
           20:"Manoeuvre de stationnement",
           21:"Manoeuvre d'évitement",
           22:"Ouverture de porte",
           23:"Arrière (hors stationnement)",
           24:"En stationnement (avec occupants)",
           25:"Circulant sur trottoir",
           26:"Autres manoeuvres"}
   
    df['Manoeuvre principale'] = df['Manoeuvre principale'].map(dico_manoeuvre)
   
    
    vehicules=df[categorie].dropna()
    #st.dataframe(accidents)

    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    plot_countplot(df=vehicules,
               col='Catégorie véhicule',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("Catégorie véhicule",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    plot_countplot(df=vehicules,
               col='Obstacle rencontré',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("Obstacle rencontre",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    plot_countplot(df=vehicules,
               col='Obstacle mobile rencontré',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("Obstacle mobile rencontré",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    plot_countplot(df=vehicules,
               col='Point choc initial',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("Point choc initial",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    plot_countplot(df=vehicules,
               col='Manoeuvre principale',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("Manoeuvre principale",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    
   
    
  
    

def pave_caracteristiques(df,annee,couleur):
    
    df = df[(df['an'] == annee)]
    
    categorie = ['agglomeration', 'vitesse_maximale_autorisee','categorie_route','sens_circulation','nombres_voies','etat_surface']
    
    dico = {
        'agg': 'agglomeration',
        'vma': 'vitesse_maximale_autorisee',
        'catr': 'categorie_route',
        'circ': 'sens_circulation',
        'nbv': 'nombres_voies',
        'surf': 'etat_surface'
  
        }

    df.rename(columns=dico, inplace=True)
    
    dico_route = {1: "Autoroute",
              2: "route nationale",
              3: "route Départementale",
              4: "voie_communale",
              5: "Hors réseau public",
              6: "Parc de stationnement",
              7: "Routes de métropole urbaine",
              9: "autre type route"}
    

    df['categorie_route'] = df['categorie_route'].map(dico_route)
    
    dico_agglo  = {1: "Hors agglomération",
              2: "En agglomération"}
    
    df['agglomeration'] = df['agglomeration'].map(dico_agglo)
    
    dico_Regime_circulation = {-1: "Non renseigné",
              1: "A sens unique",
              2: "Bidirectionnelle",
              3: "A chaussées séparées",
              4: "Avec voies d’affectation variable"
                  }
    df['sens_circulation'] = df['sens_circulation'].map(dico_Regime_circulation)
  
    
    
    dico_surface = {-1: "Non renseigné",
              1: "Normale",
              2: "Mouillée",
              3: "Flaques",
              4: "Inondée",
              5: "Enneigée",
              6: "Boue",
              7: "Verglacée",
              8: "Corps gras – huile",
              9: "Autre"}
    
    
    df['etat _surface'] = df['etat_surface'].map(dico_Regime_circulation)


    accidents=df[categorie].dropna()
    #st.dataframe(accidents)

    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    plot_countplot(df=accidents,
               col='vitesse_maximale_autorisee',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("Vitesse maximale autorisée",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
   
    plot_countplot(df=accidents,
               col='categorie_route',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10)
    
    plt.title("Categorie route",
          loc="center", fontsize=10, fontstyle='italic')
    
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    plot_countplot(df=accidents,
               col='sens_circulation',
               order=True,
               palette=[couleur],
               ax=ax, orient='h',
               size_labels=10,title="sens_circulation")
    
    plt.title("sens_circulation",
          loc="center", fontsize=10, fontstyle='italic')
    
    
    st.pyplot(fig)
    
      
    
def Affichage():
    
    # Chargement des données
   
    df_accidents_76 = pd.read_csv('data/df_SeineMaritime_Accidents_2005_2023.csv')
    df_Accidents_Usagers_France = pd.read_csv('data/df_Accidents_Usagers_76_lat_long.csv',low_memory=False) 
    df_Accidents_Usagers_76 = df_Accidents_Usagers_France[df_Accidents_Usagers_France.dep == 76]
    
    data_Accidents_lieux_76 = pd.read_csv('data/data_Accidents_lieux_76.csv')
    data_Accidents_lieux_usagers_76 = pd.read_csv('data/data_Accidents_lieux_usagers_76.csv',low_memory=False)
    
    data_Accidents_lieux_usagers_vehicule_76 = pd.read_csv('data/data_Accidents_lieux_usagers_vehicule_76.csv',low_memory=False)
    data_Accidents_lieux_vehicules_76 = pd.read_csv('data/data_Accidents_lieux_vehicules_76.csv',low_memory=False)
        
    annee = affichage_annee_filtres(df_accidents_76)
    selection = st.selectbox("Selection", ["Accidents","Blessés légers", "Blessés hospitalisés","Tués"])
    
    st.title(":red_car: Lieux des " + selection + " en Seine Maritime pour l'année " + str(annee))
    st.markdown("### En vert les " + selection + " , en rouge les positions des radards fixes")
    
    radars =  pd.read_csv('data/radars.csv')
    
    if selection:
        if selection == "Accidents":
            display_map(df_accidents_76,radars, annee)
            
            couleur = '#b0cadc'
            pave_Arrondissement(data_Accidents_lieux_76,annee,couleur)    
            pave_caracteristiques(data_Accidents_lieux_76,annee,couleur)
            
            pave_vehicule(data_Accidents_lieux_vehicules_76,annee,couleur)
            
        elif selection == "Blessés légers":
            df_accidents_Blessures_legeres = df_Accidents_Usagers_76[df_Accidents_Usagers_76.grav == 4]
            display_map(df_accidents_Blessures_legeres,radars, annee)
            
            data_Accidents_lieux_usagers_76_blesses_legers = data_Accidents_lieux_usagers_76[data_Accidents_lieux_usagers_76.grav == 4]
            couleur = '#f5b005'
            pave_Arrondissement(data_Accidents_lieux_usagers_76_blesses_legers,annee,couleur)  
            pave_caracteristiques(data_Accidents_lieux_usagers_76_blesses_legers,annee,couleur)
            
            data_Accidents_lieux_usagers_vehicule_76_bl = data_Accidents_lieux_usagers_vehicule_76[data_Accidents_lieux_usagers_vehicule_76.grav == 4] 
            
            pave_vehicule(data_Accidents_lieux_usagers_vehicule_76_bl,annee,couleur)
            
        elif selection == "Blessés hospitalisés":
            df_accidents_Blessures_hospitalises = df_Accidents_Usagers_76[df_Accidents_Usagers_76.grav == 3]
            display_map(df_accidents_Blessures_hospitalises,radars, annee)
            
            data_Accidents_lieux_usagers_76_blesses_hospitalises = data_Accidents_lieux_usagers_76[data_Accidents_lieux_usagers_76.grav == 3]
            couleur = '#f58405'
            pave_Arrondissement(data_Accidents_lieux_usagers_76_blesses_hospitalises,annee,couleur)      
            pave_caracteristiques(data_Accidents_lieux_usagers_76_blesses_hospitalises,annee,couleur)
            
            data_Accidents_lieux_usagers_vehicule_76_bh = data_Accidents_lieux_usagers_vehicule_76[data_Accidents_lieux_usagers_vehicule_76.grav == 3] 
            
            pave_vehicule(data_Accidents_lieux_usagers_vehicule_76_bh,annee,couleur)
            
        elif selection == "Tués":
            df_accidents_Tues = df_Accidents_Usagers_76[df_Accidents_Usagers_76.grav == 2]
            display_map(df_accidents_Tues,radars, annee)
            
            data_Accidents_lieux_usagers_76_tues = data_Accidents_lieux_usagers_76[data_Accidents_lieux_usagers_76.grav == 2]
            couleur = '#f50514'
            pave_Arrondissement(data_Accidents_lieux_usagers_76_tues,annee,couleur)      
            pave_caracteristiques(data_Accidents_lieux_usagers_76_tues,annee,couleur)
            
            data_Accidents_lieux_usagers_vehicule_76_tues = data_Accidents_lieux_usagers_vehicule_76[data_Accidents_lieux_usagers_vehicule_76.grav == 2] 
            
            #data_Accidents_lieux_usagers_vehicule_76_tues=df[categorie].dropna()
           
            #st.dataframe(data_Accidents_lieux_usagers_vehicule_76_tues)
            
            
            pave_vehicule(data_Accidents_lieux_usagers_vehicule_76_tues,annee,couleur)
            
        
       
    
    
Affichage()