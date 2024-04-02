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

def get_numero_segment_by_axe(df, axe):
    """
    Cette fonction retourne la liste des Numero_segment uniques pour un Axe donné.
    
    :param df: DataFrame contenant les données
    :param axe: Le nom de l'Axe pour lequel obtenir les Numero_segment
    :return: Liste des Numero_segment uniques pour l'Axe donné
    """
    filtered_df = df[df['Axe'] == axe]
    unique_segments = filtered_df['Numero_segment'].unique().tolist()
    return unique_segments


Base_indicateurs=pd.read_csv("data/Base_indicateurs.csv",sep=";")

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

st.markdown("#  <center> :clipboard: Qualité de l'offre V2 :clipboard: </center> ", unsafe_allow_html=True)  

st.write("La qualité du transport TER peut être évaluée par des indicateurs comme le nombre de circulation.")

#st.dataframe(Base_indicateurs)



liste_axe = list(Base_indicateurs["Axe"].unique())


liste_axe = st.selectbox(
   "Sélection axes",
   liste_axe,
   index=None,
)


if (liste_axe==None):
   Base_indicateurs_requete=Base_indicateurs 
   Texte1=""
   Texte2="Global"
   color="Axe"
else :
  Base_indicateurs_requete=Base_indicateurs[Base_indicateurs["Axe"]==liste_axe]
  axe = liste_axe 
  segments_axes =  get_numero_segment_by_axe(Base_indicateurs, axe)
  #segments_axes = list(Base_indicateurs["Numero_segment"].unique())
  selectbox_segment = st.selectbox( 
    'Sélection des segments',
    segments_axes ,index=None)
  Texte1=" sur l'axe "+str(liste_axe) 
  Texte2=str(liste_axe)
  color="Numero_segment"
  if (selectbox_segment==None):
       Base_indicateurs_requete=Base_indicateurs[Base_indicateurs["Axe"]==liste_axe]
  else :
       Base_indicateurs_requete=Base_indicateurs[Base_indicateurs["Numero_segment"]==selectbox_segment]
       Texte1=" sur le segment "+str(selectbox_segment) 
       Texte2=str(selectbox_segment) 
       color="Numero_train"

    





# Création de l'histogramme avec Plotly
fig = px.histogram(Base_indicateurs_requete, x='Mois', y='Estimation_Nombre_circulation', title='Nombre de circulation par mois'+Texte1,  color=color,
                   category_orders={"Mois": ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']})

fig.update_yaxes(title="Nombre de circulations")






# Affichage du graphique
st.plotly_chart(fig)

#st.write(liste_segment)
#Base_circulation_requete=Base_circulation[Base_circulation["Numero_segment"]==liste_segment]


Base_indicateurs["Numero_train"]=Base_indicateurs["Numero_train"].astype(str)



# Calcul du total des circulations pour chaque numéro de train
df=Base_indicateurs_requete
# Ordre des mois en français
mois_ordre = {"janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7, "août": 8, "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12}

# Transformation des données
grouped = df.groupby(['Mois', 'Numero_train'])['Estimation_Nombre_circulation'].sum().reset_index()
total_circulations_per_month = grouped.groupby('Mois')['Estimation_Nombre_circulation'].sum().reset_index(name='Total_Nombre_Circulations')
couples_per_month = grouped.groupby('Mois').apply(
    lambda x: ", ".join(f"({num}, {circ})" for num, circ in zip(x.Numero_train, x.Estimation_Nombre_circulation))
).reset_index(name='Couples_Numero_TER_Circulations')

# Fusion des résultats
final_result_df = pd.merge(total_circulations_per_month, couples_per_month, on='Mois')

# Ajouter une colonne temporaire pour l'ordre des mois
final_result_df['Ordre_Mois'] = final_result_df['Mois'].map(mois_ordre)

# Trier par cette colonne temporaire
final_result_df = final_result_df.sort_values(by='Ordre_Mois')

# Supprimer la colonne temporaire
final_result_df = final_result_df.drop(columns=['Ordre_Mois'])
# Vous pouvez maintenant tenter de visualiser df_final dans Streamlit sans rencontrer l'erreur
st.dataframe(final_result_df)

st.download_button(
    label="Exporter en CSV",
    data=final_result_df.to_csv(sep=';',index=False,encoding='utf-8-sig').encode('utf-8-sig'),
    file_name='Indicateurs_circulation_'+str(Texte2).replace(" ","_")+'.csv',
    mime='text/csv',
    )




