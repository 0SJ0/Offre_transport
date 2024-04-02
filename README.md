[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sj-hdf-offre-ter-hdf-bienvenue-37vqxq.streamlit.app/)
[![Python](https://img.shields.io/badge/python-v3.8-blueviolet)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/plotly-5.10.0-blue)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/pandas-1.4-blue)](https://pandas.pydata.org/)
[![Requests](https://img.shields.io/badge/requests-2.31.0-blue)](https://docs.python-requests.org/)


# Offre TER HdF

Cette application propose de visualiser l'offre TER dans la region des Hauts-de-France. On peut connaitre les correspondances des TER, obtenir des informations sur les points d'arrêt et télécharger un fichier GTFS régional.

Lien du projet déployé : " https://sj-hdf-offre-ter-hdf-bienvenue-37vqxq.streamlit.app/ "

# Contenu du dépot

```
├── data
│   ├── liste_gares.csv
│   ├── Liste_gares_geo.csv
│   └── gtfs
├── docs
│   ├── LICENSE.txt
│   ├── guide_application_offre_streamlit.pdf
├── pages
│   ├── Correspondances.py
│   ├── Extraction_offre.py
│   ├── Fiches_gares.py
│   ├── Qualité_offre.py
│   ├── Isochrone.py
│   └── GMAO.py
├── Bienvenue.py
├── README.md
├── packages.txt
└── requirements.txt
```

# Installation et exécution

Pour déployer cette application Streamlit en local :

**1 - Clonez ce repo sur votre machine :**

```
git clone https://path/Offre_TER_HdF.git
```

**2 - Naviguez jusqu'au dossier du repo :**

```
cd Offre_TER_HdF.git
```

**3 - (Optionnel) Créez un environnement virtuel pour isoler les dépendances :**

```
python -m venv venv
```

**4 - Activez l'environnement virtuel :**

Sur Windows :
```
.\venv\Scripts\activate
```
Sur macOS et Linux :
```
source venv/bin/activate
```
**5 - Installez les dépendances nécessaires :**

```
pip install -r requirements.txt
```
**6 - Lancez l'application Streamlit :**

```
streamlit run Bienvenue.py
```
**7 - Accédez à l'application dans un navigateur :**

L'application devrait être accessible à l'adresse suivante : http://localhost:8501

**8- Pour arrêter l'application :**

Appuyez sur Ctrl+C dans le terminal.

# Utilisation

L'application ouvre sur un menu. Il suffit de selectionner le projet recherché sur la barre de navigation.

# Dépendances


```
pandas >=1.4
seaborn >=0.11
streamlit >= 1.12.0
matplotlib >= 3.1
plotly >= 5.10.0
requests >= 2.31.0 
beautifulsoup4 >= 4.12.2 
fuzzywuzzy >= 0.18.0 
pytz >= 2023.3 
folium >= 0.14.0 
streamlit_folium >=0.13.0 
openrouteservice >= 2.3.3
geopy >= 2.4.0 
```


# Licence

GPL-3.0 license docs/LICENSE.txt








