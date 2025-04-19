import streamlit as st
import pandas as pd
import pydeck as pdk
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def page_two():
    st.write("Diese Jobs gibt es in deiner Region")

# ----------------------------
# Hilfsfunktion: Anhand der variable address die Koordinaten Latitude und Longitude ermitteln
# ----------------------------
def get_coords_from_address(address):
    geolocator = Nominatim(user_agent="job_app")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None

# ----------------------------
# Filtert Jobs im angegebenen Umkreis (angegeben in km)
# ----------------------------
def filter_jobs_within_radius(center_coords, radius_km):
    nearby_jobs = []
#    for _, job in NAME DES DATENSATZES(): 
        job_coords = (job['lat'], job['lon'])
        distance = geodesic(center_coords, job_coords).km
        if distance <= radius_km:
            nearby_jobs.append(job)
    return pd.DataFrame(nearby_jobs)


# Streamlit UI
st.title("Aktuelle Jobs in deiner Nähe")

address = st.text_input("Ort eingeben", "Zürich")
radius = st.slider("Umkreis auswählen (km)", min_value=5, max_value=100, value=25)

