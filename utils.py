# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 21:38:24 2024

@author: lebri
"""

import streamlit as st
import pandas as pd
import os


def chargement_donnees(annee):
    return annee

def alignement(text):
    for _ in range(text):
        st.write("\n")