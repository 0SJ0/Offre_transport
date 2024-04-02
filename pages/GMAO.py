import streamlit as st
import pandas as pd

st.markdown("#  <center> 		:male-mechanic:  GMAO		:male-mechanic: </center> ", unsafe_allow_html=True)  

st.write("La GMAO est une méthode / outil de gestion de la maintenance par le biais d’un logiciel permettant de gérer les différentes tâches la maintenance des équipements au sein d’une entité (entreprise, collectivité, administration…)")

st.write("Sélection de l'objectif :")

Approche_vehicules = st.checkbox("Constuire un état des lieux du parc des véhicules ferroviaires enregistrés.")


Approche_organes = st.checkbox("Connaître les règles de maintenance des organes.")


    
    
Approche_operations = st.checkbox("Connaître les coûts des opérations de maintenance")


if Approche_vehicules:
    st.markdown("### Etat  des lieux du matériel roulant :")
    
    st.write(" Au total nous avons 3  véhicules ferroviaires enregistrés âgés entre 2010 et 2021")
    
    Selectbox_vehicule = st.selectbox(
    'Liste des véhicules ferroviaires enregistrés :',
    ('Rame 1', 'Rame 2', 'Remorque 1'))
    
    st.write('Véhicule selectionné :', Selectbox_vehicule)
    st.markdown("- Informations descriptives (Age, type véhicule)")
    st.markdown("- Téléchargement du certificat d'immatriculation")
    st.markdown("- Scan de la rame sur l'état des organes via un score, si le véhicule selectionné est une rame ") 

if Approche_organes:
    st.markdown("### Règles de maintenance des organes :")
    
    st.write(" Au total nous avons 3 types d'organes de maintenance")
    # Nous disposons de 3 véhicules ferrés agés entre 2010 et 2019
    
    Selectbox_organe = st.selectbox(
    'Liste des organes :',
    ('Organe 1', 'Organe 2', 'Organe 3'))
    
    st.write('Organe selectionné :', Selectbox_organe)
    st.markdown("- Nombres d'organes enregistrés")
    st.markdown(" - Pas de maintenance ")
    st.markdown(" - Téléchargement des documents relatifs à cet organe ")

if Approche_operations:
    st.markdown("### Coûts des opérations de maintenance :")
    st.write("(en construction)")

