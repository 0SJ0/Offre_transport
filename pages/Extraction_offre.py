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
# Data visualisation
import plotly.express as px
import streamlit as st
from PIL import Image
# Traitement texte
from bs4 import BeautifulSoup
import re

#################################################################### Début application ################################################################

# Chargement des gares pour le filtrage
df_gares=pd.read_csv("data/liste_gares.csv", sep=';')
liste_code_UIC_1 = list(df_gares["code_uic_complet"].unique())
liste_code_UIC = liste_code_UIC_1 + [str(i) for i in liste_code_UIC_1] + ["00" + str(i) for i in liste_code_UIC_1] + [str(i)[2:] for i in liste_code_UIC_1] + [str(i) for i in [str(i)[2:] for i in liste_code_UIC_1]] # Variation de l'écriture des codes UIC

# Presentation application
st.markdown("#  <center> 	:pick:  Extraction de l'offre TER	:pick: </center> ", unsafe_allow_html=True)  
st.write("Ci-dessous un bouton pour télécharger la dernière version du  GTFS à une échelle régionale.")


# Lien SNCF GTFS
url = "https://eu.ftp.opendatasoft.com/sncf/gtfs/export-ter-gtfs-last.zip"
filename = "GTFS_HdF.zip"

# Bouton GTFS
if st.button('Télécharger le GTFS régional des HdF'):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            gtfs_data = response.content
            b64 = base64.b64encode(gtfs_data).decode()
            stop_times_processed = False
            stops_processed = False
            trips_processed = False
            routes_processed = False
            calendar_dates_processed =False
            feed_info_processed = False
            agency_processed = False
            transfers_processed = False            
            liste_zip=["stop_times.txt","stops.txt","trips.txt","routes.txt","calendar_dates.txt","feed_info.txt","agency.txt","transfers.txt"]                    
            with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
                for filename in liste_zip:
                    zip_ref.extract(filename, "GTFS_HdF")
                st.write("Voici la composition du GTFS :")
                # Create a dictionary that maps each filename to its index in liste_zip
                index_dict = {filename: index for index, filename in enumerate(liste_zip)}
                 # Get a list of ZipInfo objects and sort them based on their index in the dictionary
                sorted_files = sorted(zip_ref.infolist(), key=lambda x: index_dict[x.filename])
                for element_archive in sorted_files:
                    st.text(element_archive.filename)
                    if element_archive.filename == 'stop_times.txt':
                        stop_times = pd.read_csv(zip_ref.open('stop_times.txt'))
                        stop_times['uic'] = stop_times['stop_id'].str[-8:]
                        stop_times = stop_times[stop_times['uic'].isin(liste_code_UIC)]
                        stop_times = stop_times.drop('uic', axis=1)
                        stop_times.to_csv("stop_times.txt", index=False)
                        # Extraction des trip_id
                        liste_trips_id=list(stop_times.trip_id)
                        stop_times_processed = True
                    if element_archive.filename == 'stops.txt':
                        stops = pd.read_csv(zip_ref.open('stops.txt'))
                        stops['uic'] = stops['stop_id'].str[-8:]
                        stops = stops[stops['uic'].isin(liste_code_UIC)]
                        stops = stops.drop('uic', axis=1)
                        stops.to_csv("stops.txt", index=False)
                        stops_processed = True     
                    if element_archive.filename == 'trips.txt':
                        trips = pd.read_csv(zip_ref.open('trips.txt'))
                        #Filtrage
                        trips=trips[trips['trip_id'].isin(liste_trips_id)]
                        # Extraction des routes et services
                        liste_route_id=list(trips.route_id)
                        liste_service_id=list(set(trips.service_id))
                        trips.to_csv("trips.txt", index=False)
                        trips_processed = True                       
                    if element_archive.filename == 'routes.txt':
                        routes=pd.read_csv(zip_ref.open('routes.txt'))
                        #st.dataframe(routes)
                        #Filtrage
                        routes=routes[routes['route_id'].isin(liste_route_id)] # Problème d'ordre chronologique
                        #routes=routes[routes['route_id'].isin(liste_route_id)]
                        # Extraction des agences
                        liste_agency_id=list(set(routes.agency_id))
                        routes.to_csv("routes.txt", index=False)
                        routes_processed = True
                    if element_archive.filename == 'calendar_dates.txt':
                        calendar_dates=pd.read_csv(zip_ref.open('calendar_dates.txt'))
                        #Filtrage
                        calendar_dates=calendar_dates[calendar_dates['service_id'].isin(liste_service_id)]
                        calendar_dates.to_csv("calendar_dates.txt", index=False)
                        calendar_dates_processed = True                        
                    if element_archive.filename == 'feed_info.txt':
                        feed_info = pd.read_csv(zip_ref.open('feed_info.txt'))
                        feed_info.to_csv("feed_info.txt", index=False)
                        feed_info_processed = True                        
                    if element_archive.filename == 'agency.txt':
                        agency=pd.read_csv(zip_ref.open('agency.txt'))
                        #Filtrage
                        agency=agency[agency['agency_id'].isin(liste_agency_id)]
                        agency.to_csv("agency.txt", index=False)
                        agency_processed = True                        
                    if element_archive.filename == 'transfers.txt':
                        transfers=pd.read_csv(zip_ref.open('transfers.txt'))
                        transfers.to_csv("transfers.txt", index=False)
                        transfers_processed = True                        
            with zipfile.ZipFile('GTFS_HdF2.zip', mode='w') as archive:
                if stop_times_processed:
                    archive.write('stop_times.txt')
                if stops_processed:
                    archive.write('stops.txt')
                if trips_processed:
                    archive.write('trips.txt')
                if routes_processed:
                    archive.write('routes.txt')
                if calendar_dates_processed:
                    archive.write('calendar_dates.txt')
                if feed_info_processed:
                    archive.write('feed_info.txt')
                if agency_processed:
                    archive.write('agency.txt')
                if transfers_processed:
                    archive.write('transfers.txt')
            # Générer un lien de téléchargement pour le nouveau fichier zip
            with open("GTFS_HdF2.zip", "rb") as f:
                gtfs_data = f.read()
            b64 = base64.b64encode(gtfs_data).decode()
            href = f'<a href="data:application/zip;base64,{b64}" download="GTFS_HdF2.zip">Cliquez ici pour télécharger le fichier GTFS des HdF.</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.write(f"Erreur lors du téléchargement du fichier : {response.status_code}")
    except:
        st.write("Erreur")

# Affichage des gares utilisées pour le filtrage
st.markdown("## Comment est généré le GTFS régional ?", unsafe_allow_html=True)  
st.write("Le GTFS national fourni par l'opendata de la SNCF est téléchargé et filtré à partir d'une selection de points d'arrêt. Voici la liste des points d'arrêt utilisée :")
liste_gares=list(df_gares.nom_gare.values)
Gare = st.selectbox("Liste des points d'arrêts",liste_gares)

#################################################################### Fin application ################################################################

# On peut imaginer un même bouton pour les autres types d'offre au format Netex ou autres.
