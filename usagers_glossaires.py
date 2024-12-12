# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 16:04:09 2024

@author: lebri
"""

usagers_glossaires = {
    'Num_Acc':"Numéro d'identifiant de l'accident.",
    'place':"Place dans la voiture",
    'catu':"Catégorie d'usager",
    'grav':"Gravité de blessures",
    'sexe':"Sexe d el'usager",
    'trajet':"Motif de déplacement au moment de l'accident",
    'secu':"Equipement de sécurité",
    'locp':"Localisation du pieton",
    'actp':"Action du piéton",
    'etatp':"Piéton accidenté seul ou non",
    'an_nais':"Année d enaissance de l'usager",
    'num_veh':"Identifiant du véhicule"
    }

usagers_indices = {
    'grav':{1:"Indemne",
           2:"Tué",
           3:"Blessé hospitalisé",
           4:"Blessé léger"
        },
    'sexe':{1:"Masculin",
           2:"Féminin"
        },
    'trajet':{1:"Domicile – travail",
           2:"Domicile – école",
           3:"Courses – achats",
           4:"Utilisation professionnelle",
           5:"Promenade – loisirs",
           9:"Autre",
        },
    
   
 }