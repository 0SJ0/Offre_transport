# Librairies
# Calcul
import numpy as np
import math
# Data management
import zipfile
from datetime import datetime, timedelta
import base64
import json
import pandas as pd
import io
import requests
import shutil
from fuzzywuzzy import process
# Data visualisation
import plotly.express as px
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
# Traitement texte
from bs4 import BeautifulSoup
import re
import random
import pytz

st.set_page_config(initial_sidebar_state="collapsed")

@st.cache_data
def import_dataset(nom,opendata="sncf"):
    """Importe un jeu de données issues de l'open data de la SNCF"""
    requete='https://ressources.data.sncf.com/api/v2/catalog/datasets/'+str(nom)+"/exports/json?limit=-1&offset=0&timezone=UTC"
    API_requete = requests.get(requete)
    reponse=API_requete.json()
    df=pd.DataFrame(reponse)
    return(df)

formule_regularite = r'''
#### Formule :
$$ 
Taux\ de\ régularité =  (\frac{(Nombre\ de\ trains\ ayant\ circulé - Nombre\ de\ trains\ en\ retard\ à\ l'arrivée)}{Nombre\ de\ trains\ ayant\ circulé}) \cdot 100 
$$

'''

formule_suppression = r'''
#### Formule :
$$ 
Taux\ de\ suppression = (1 - ( \frac{Nombre\ de\ trains\ ayant\ circulé }{Nombre\ de\ trains\ programmés})) \cdot 100
$$

'''


#### Début application ###

st.markdown("#  <center> :clipboard: Qualité de l'offre :clipboard: </center> ", unsafe_allow_html=True)  

st.write("La qualité du transport TER peut être évaluée par des indicateurs comme le taux de régularité et le taux de suppression.")

#
df_regularite=import_dataset("regularite-mensuelle-ter")
df_regularite=df_regularite[df_regularite["region"]=="Hauts-de-France"]
df_regularite['annee'] = df_regularite['date'].str.split('-').str[0]
df_regularite['mois'] = df_regularite['date'].str.split('-').str[1]
df_regularite=df_regularite[['annee','mois','nombre_de_trains_programmes','nombre_de_trains_ayant_circule','nombre_de_trains_en_retard_a_l_arrivee']]

df_regularite["Taux_suppression"]=round(100-df_regularite['nombre_de_trains_ayant_circule']*100/df_regularite['nombre_de_trains_programmes'],2)
df_regularite["Taux_regularite"]=round((df_regularite['nombre_de_trains_ayant_circule']-df_regularite['nombre_de_trains_en_retard_a_l_arrivee'])*100/df_regularite['nombre_de_trains_ayant_circule'],2)

unique_values = df_regularite["annee"].unique()
liste = [int(value) for value in unique_values]

#

df_regularite_max_annee=df_regularite[df_regularite["annee"]==str(max(liste))].sort_values(by="mois").iloc[-1]
#st.dataframe(df_regularite_max_annee)

annee_last=df_regularite_max_annee.annee
month_last=df_regularite_max_annee.mois
programmes_last=df_regularite_max_annee.nombre_de_trains_programmes
suppression_last=df_regularite_max_annee.Taux_suppression
regularite_last=df_regularite_max_annee.Taux_regularite
message_final_1=str(month_last)+"/"+str(annee_last)
message_final_2=str(int(programmes_last))+ " trains sont programmés, le taux de suppression est de "+str(suppression_last)+"% et le taux de régularité est de "+ str(regularite_last)+ "%."

st.markdown("Pour info, au " + message_final_1 +" , " +message_final_2, unsafe_allow_html=True) 
#





Noms_taux = st.multiselect( 
    'Sélection des métriques de qualité',
    ['Taux de régularité','Taux de suppression','Nombre de circulations'],
    []) # 'Généralités', 'Photo',





Start_annee = st.slider(
    "Choix d'une année ",
    min(liste),max(liste),max(liste))
#st.dataframe(df_regularite)

if('Nombre de circulations' in list(Noms_taux)):  
    st.markdown("#  <center> :stopwatch: Nombre de circulations :stopwatch: </center> ", unsafe_allow_html=True)  
    st.write("Le Nombre de circulations correspond au nombre de trains ayant circulés.")

    

    df_regularite=df_regularite[df_regularite["annee"]==str(Start_annee) ].sort_values(by="mois")
    Liste_mois=list(df_regularite["mois"])
    Liste_taux=list(df_regularite["Taux_regularite"])
    Liste_circule=list(df_regularite["nombre_de_trains_ayant_circule"])
    Liste_retard=list(df_regularite['nombre_de_trains_en_retard_a_l_arrivee'])
    
    df_plotly_regularite = pd.DataFrame(dict(
    Mois = Liste_mois,
    Taux = Liste_taux,
    Nombre_de_trains_ayant_circulé=Liste_circule,
    Nombre_de_trains_en_retard_a_l_arrivee=Liste_retard 
    ))
    # Supposons que df_plotly_regularite est votre DataFrame
    # Remplacer les chiffres des mois par des noms
    mois_noms = {"01": 'Janvier', "02": 'Février', "03": 'Mars', "04": 'Avril', "05": 'Mai', "06": 'Juin', 
             "07": 'Juillet', "08": 'Août', "09": 'Septembre', "10": 'Octobre', "11": 'Novembre', "12": 'Décembre'}
    df_plotly_regularite['Mois'] = df_plotly_regularite['Mois'].replace(mois_noms)


    fig = px.histogram(df_plotly_regularite, x='Mois', y='Nombre_de_trains_ayant_circulé', title='Evolution du nombre de circulations par mois',
                   category_orders={"Mois": ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']})

    # Mise à jour des axes si nécessaire
    fig.update_xaxes(categoryorder='array', categoryarray= list(mois_noms.values()))
    fig.update_yaxes(title="Nombre de circulations")

    # Affichage de la figure
    st.plotly_chart(fig)
    


if('Taux de régularité' in list(Noms_taux)):  
    st.markdown("#  <center> :stopwatch: Taux de régularité :stopwatch: </center> ", unsafe_allow_html=True)  
    st.write("Le taux de régularité correspond au pourcentage des trains arrivant à l'heure parmi les trains ayant circulés.")

    

    df_regularite=df_regularite[df_regularite["annee"]==str(Start_annee) ].sort_values(by="mois")
    Liste_mois=list(df_regularite["mois"])
    Liste_taux=list(df_regularite["Taux_regularite"])
    Liste_circule=list(df_regularite["nombre_de_trains_ayant_circule"])
    Liste_retard=list(df_regularite['nombre_de_trains_en_retard_a_l_arrivee'])
    
    df_plotly_regularite = pd.DataFrame(dict(
    Mois = Liste_mois,
    Taux = Liste_taux,
    Nombre_de_trains_ayant_circulé=Liste_circule,
    Nombre_de_trains_en_retard_a_l_arrivee=Liste_retard 
    ))
    df_plotly_regularite = df_plotly_regularite.sort_values(by="Mois")
    fig = px.line(df_plotly_regularite, x="Mois", y="Taux", title="Evolution du taux de régularité",hover_data=["Nombre_de_trains_ayant_circulé","Nombre_de_trains_en_retard_a_l_arrivee"]) 
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(title="Taux de régularité")

    


    st.plotly_chart(fig)
    

    st.write(formule_regularite)

   

if('Taux de suppression' in list(Noms_taux)):  
    st.markdown("#  <center> :wave: Taux de suppression :wave: </center> ", unsafe_allow_html=True)  
    st.write("Le taux de suppresion correspond au pourcentage des trains annulés parmi les trains programmés.")



    df_regularite=df_regularite[df_regularite["annee"]==str(Start_annee) ].sort_values(by="mois")
    Liste_mois=list(df_regularite["mois"])
    Liste_taux=list(df_regularite["Taux_suppression"])
    Liste_circule=list(df_regularite["nombre_de_trains_ayant_circule"])
    Liste_programmes=list(df_regularite["nombre_de_trains_programmes"])
    df_plotly_suppression = pd.DataFrame(dict(
    Mois = Liste_mois,
    Taux = Liste_taux,
    Nombre_de_trains_ayant_circulé=Liste_circule,
    Nombre_de_trains_programmes=Liste_programmes  
    ))
    df_plotly_suppression = df_plotly_suppression.sort_values(by="Mois")
    fig = px.line(df_plotly_suppression, x="Mois", y="Taux", title="Evolution du taux de suppression",hover_data=["Nombre_de_trains_ayant_circulé","Nombre_de_trains_programmes"]) 
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(title="Taux de suppression")
    


    st.plotly_chart(fig)

    st.write(formule_suppression)
