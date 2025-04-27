import streamlit as st
import pandas as pd
import pydeck as pdk
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

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
def filter_jobs_within_radius(center_coords, radius_km, jobs):
    nearby_jobs = []
    for _, job in jobs.iterrows():
        job_coords = (job['lat'], job['lon'])
        distance = geodesic(center_coords, job_coords).km
        if distance <= radius_km:
            nearby_jobs.append(job)
    return pd.DataFrame(nearby_jobs)

def page_two():
    st.title("Aktuelle Jobs in deiner Nähe")

    address = st.text_input("Ort eingeben", "Zürich")
    radius = st.slider("Umkreis auswählen (km)", min_value=5, max_value=100, value=25)

    if address:
        coords = get_coords_from_address(address)
        if coords:
            filtered_jobs = filter_jobs_within_radius(coords, radius, job_data)

            if not filtered_jobs.empty:
                st.map(filtered_jobs[['lat', 'lon']])

                # Zusätzlich: Details als Tabelle anzeigen
                st.subheader("Gefundene Jobs")
                st.dataframe(filtered_jobs[['title', 'company']])

                # Schönere Karte mit pydeck
                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=filtered_jobs,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=2000,
                )

                view_state = pdk.ViewState(
                    latitude=coords[0],
                    longitude=coords[1],
                    zoom=8,
                    pitch=0,
                )

                r = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    tooltip={"text": "{title} bei {company}"}
                )

                st.pydeck_chart(r)

            else:
                st.warning("Keine Jobs im angegebenen Umkreis gefunden.")
        else:
            st.error("Adresse konnte nicht gefunden werden. Bitte versuche es erneut.")


page_two()
