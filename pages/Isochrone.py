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
import openrouteservice
# Data visualisation
import plotly.express as px
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
import geopy.distance
import random



# Traitement texte
from bs4 import BeautifulSoup
import re


st.set_page_config(initial_sidebar_state="collapsed")

def get_closest_point_on_road(lat, lon, radius=100):
    # Requête Overpass pour trouver les routes à proximité
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    way(around:{radius},{lat},{lon})["highway"];
    (._;>;);
    out body;
    """
    
    response = requests.get(overpass_url, 
                            params={'data': overpass_query})
    data = response.json()
    
    if not data['elements']:
        raise ValueError("Aucun chemin trouvé à proximité. Augmentez le rayon de recherche.")
    
    closest_distance = float('inf')
    closest_coords = None
    
    for element in data['elements']:
        if element['type'] == 'node':
            node_lat = element['lat']
            node_lon = element['lon']
            distance = geopy.distance.distance((lat, lon), (node_lat, node_lon)).m
            if distance < closest_distance:
                closest_distance = distance
                closest_coords = (node_lat, node_lon)
    
    return closest_coords

#####

df_gares=pd.read_csv("data/Liste_gares_geo.csv", sep=';')
df_gares=df_gares[["CODE_UIC","LIBELLE","GeoPoint"]]
df_gares=df_gares.drop_duplicates(subset=["CODE_UIC", "LIBELLE"], keep="first")
#df_gares=df_gares.drop_duplicates()

liste_gares= sorted(list(df_gares.LIBELLE.values))

st.markdown("#  <center> :woman-running: Isochrone 	:man-running: </center> ", unsafe_allow_html=True)  

st.markdown(" Une zone isochrone est l'ensemble des lieux que l'on peut atteindre en une durée définie à partir d'un point géographique.")

st.markdown("L'ambition de ce programme est de créer un simulateur de zone isochrone à partir d'un point géographique dans les Hauts-de-france et via des modes de transport intermodaux.")


Gare_depart = st.selectbox('Sélection de la gare de départ',liste_gares)



Modes = st.multiselect(
    'Selection des modes autorisés de transport',
    ['trains', 'à pied','vélo'],
    ['à pied'])

Duree = st.slider('Selection de la durée ',5, 180, 60, step=5)
st.write('Temps :', Duree, " minutes.")

st.markdown("##  Isochrone :", unsafe_allow_html=True)
            
API_KEY = '5b3ce3597851110001cf6248ebf8c988a2a54b2e893c32d1c326fc03'  

# Récupération coordonnées ville 


coordonnees= df_gares.loc[df_gares["LIBELLE"] == Gare_depart, "GeoPoint"].values[0]


latitude = float(coordonnees.split(',')[0])
longitude =  float(coordonnees.split(',')[1])


def draw_isochrone(api_key, coord, duration,Gare_depart , Mode):
    client = openrouteservice.Client(key=api_key)
    
    # Calculer l'isochrone
    if (Mode==["à pied"]) :
        isochrones = client.isochrones(
            locations=[coord[::-1]],  # inversion des coordonnées ici pour l'API
            profile='foot-walking',
            range=[duration],
            interval=duration,
            location_type='start'
        )
        m = folium.Map(location=coord, zoom_start=10)  # coordonnées non inversées pour folium
        
    else :
            isochrones = client.isochrones(
                locations=[coord[::-1]],  # inversion des coordonnées ici pour l'API
                profile='cycling-regular',
                range=[duration],
                interval=duration,
                location_type='start'
        )
            m = folium.Map(location=coord, zoom_start=8)  # coordonnées non inversées pour folium
    
   

    folium.Marker(
        location=[latitude, longitude],
        popup="Gare "+ Gare_depart,
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)
    
    
    # Ajouter l'isochrone à la carte
    folium.GeoJson(isochrones).add_to(m)

    
    
    return m

def ajouter_bruit(latitude, longitude, bruit_max=0.001):
    """
    Ajoute un bruit aléatoire à la latitude et la longitude données.
    
    Args:
    - latitude (float): Latitude d'origine.
    - longitude (float): Longitude d'origine.
    - bruit_max (float, optional): La valeur maximale du bruit à ajouter ou soustraire. Default est 0.001.

    Returns:
    (float, float): Nouvelle latitude et longitude avec du bruit.
    """
    
    latitude_bruitee = latitude + random.uniform(-bruit_max, bruit_max)
    longitude_bruitee = longitude + random.uniform(-bruit_max, bruit_max)

    return latitude_bruitee, longitude_bruitee

try :
    latitude, longitude = ajouter_bruit(latitude, longitude, bruit_max=0.001)
    closest_point = get_closest_point_on_road(latitude, longitude)
    AMIENS_CENTER = [closest_point[0], closest_point[1]]  # Latitude, Longitude pour folium
    DURATION = Duree*60  # 1 heure en secondes
    # Afficher la carte directement dans le notebook
    map_obj = draw_isochrone(API_KEY, AMIENS_CENTER, DURATION,Gare_depart=Gare_depart, Mode=Modes)
    folium_static(map_obj)

except : 
    try :
        latitude, longitude = ajouter_bruit(latitude, longitude, bruit_max=0.002)
        closest_point = get_closest_point_on_road(latitude, longitude)
        AMIENS_CENTER = [closest_point[0], closest_point[1]]  # Latitude, Longitude pour folium
        DURATION = Duree*60  # 1 heure en secondes
        map_obj = draw_isochrone(API_KEY, AMIENS_CENTER, DURATION,Gare_depart=Gare_depart, Mode=Modes)
        folium_static(map_obj)

    except :
        try :
            latitude, longitude = ajouter_bruit(latitude, longitude, bruit_max=0.003)
            closest_point = get_closest_point_on_road(latitude, longitude)
            AMIENS_CENTER = [closest_point[0], closest_point[1]]  # Latitude, Longitude pour folium
            DURATION = Duree*60  # 1 heure en secondes
            map_obj = draw_isochrone(API_KEY, AMIENS_CENTER, DURATION,Gare_depart=Gare_depart, Mode=Modes)
            folium_static(map_obj)
        except :
            latitude, longitude = ajouter_bruit(latitude, longitude, bruit_max=0.004)
            closest_point = get_closest_point_on_road(latitude, longitude)
            AMIENS_CENTER = [closest_point[0], closest_point[1]]  # Latitude, Longitude pour folium
            DURATION = Duree*60  # 1 heure en secondes
            map_obj = draw_isochrone(API_KEY, AMIENS_CENTER, DURATION,Gare_depart=Gare_depart, Mode=Modes)
            folium_static(map_obj)
            





