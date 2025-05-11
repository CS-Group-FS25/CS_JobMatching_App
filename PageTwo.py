import streamlit as st
import requests
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# Adzuna API Einrichten mit API ID und Schlüssel
APP_ID = "42d55acf"
APP_KEY = "2fde9c1ff58d9bfdf254dd3f0c4d6ec7"
url = f'https://api.adzuna.com/v1/api/jobs/ch/search/1'


# 🔁 Funktion für Reverse-Geocoding (OpenStreetMap / Nominatim)
def get_postcode_from_coords_or_name(job):
    ort = job["location"].get("display_name")
    if ort:  ### Wenn ein Ort vorhanden ist, wird über die Nominatim API die PLZ abgerufen
        nominatim_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": ort,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        headers = {"User-Agent": "streamlit-job-app"}
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200 and r.json():  ### Bei erfolgreicher Abfrage wird die PLZ zurückgegeben
            data = r.json()[0]
            return data.get("address", {}).get("postcode", "PLZ nicht gefunden")
    return "PLZ nicht verfügbar"


def main():
    st.title("🔍 Klassische Jobsuche")
    st.markdown("Suche nach aktuellen Stellenanzeigen in der Schweiz.")

    ### Eingabefelder für die Jobsuche
    job_title = st.text_input("🔧 Stichwort (z. B. Finanzen)", "Finanzen")
    location = st.text_input("📍 Ort (z. B. Zürich)", "Zürich")
    results_per_page = st.slider("📄 Anzahl der Ergebnisse", min_value=1, max_value=20, value=5)

    ### Einrichten von Session_State
    if "suche_gestartet" not in st.session_state:
        st.session_state["suche_gestartet"] = False

    ### Button zum Auslösen der Suche
    if st.button("🔎 Jobs suchen"):
        st.session_state["suche_gestartet"] = True

    if st.button("🔄 Neue Suche starten"):
        st.session_state["suche_gestartet"] = False
        st.rerun()

        ### Wenn die Suche gestartet wurde, wird die API aufgerufen
    if st.session_state["suche_gestartet"]:
        with st.spinner("Suche läuft..."):
            ### notwendige Parameter für die API-Abfrage
            params = {
                'app_id': APP_ID,
                'app_key': APP_KEY,
                'what': job_title,
                'where': location,
                'results_per_page': results_per_page,
                'content-type': 'application/json'
            }
            ### Speichern der Antwort in einer Variablen
            response = requests.get(url, params=params)

            if response.status_code == 200:  ### Wenn die API erfolgreich abgerufen wurde, wird die Antwort verarbeitet

                data = response.json()
                results = data.get("results", [])
                if not results:
                    st.info("Keine Jobs gefunden.")

                map_data = []
                column1, column2 = st.columns(2)
                with column1:  ### Spalte 1 mit Darstellung der Jobanzeigen
                    for job in results:
                        st.subheader(job.get("title"))
                        st.write("📌 Firma:", job.get("company", {}).get("display_name", "Unbekannt"))
                        st.write("📍 Ort:", job.get("location", {}).get("display_name", ""))
                        longitude = job.get("longitude")  ### Wichtige Koordinaten für die Karte
                        latitude = job.get("latitude")
                        st.write("🌍 Koordinaten:", f"({latitude}, {longitude})")
                        if latitude is not None and longitude is not None:  ### Falls die Stellenanzeige Koordinaten ausgibt, werden diese für die Karte gespeichert
                            map_data.append({"lat": latitude, "lon": longitude})

                        st.write(job.get("description", "")[:300] + "...")
                        st.markdown(f"[🔗 Zum Job]({job.get('redirect_url')})")

                    ### PLz filtern
                    plz = get_postcode_from_coords_or_name(job)
                    # st.write("📮 PLZ:", plz)
                with column2:  ### Spalte 2 mit Darstellung der Karte
                    if map_data:
                        st.title(" Interaktive Karte")

                        center_lat = map_data[0]["lat"]
                        center_lon = map_data[0]["lon"]
                        job_map = folium.Map(
                            location=[center_lat, center_lon],
                            zoom_start=10,
                            tiles="OpenStreetMap"
                        )
                        for job in results:
                            lat = job.get("latitude")
                            lon = job.get("longitude")
                            title = job.get("title", "Kein Titel")
                            company = job.get("company", {}).get("display_name", "Unbekannt")
                            nominatim_url = job.get("redirect_url", "#")

                            if lat and lon:
                                popup_html = f"<b>{title}</b><br>{company}<br><a href='{url}' target='_blank'>Zum Job</a>"
                                folium.Marker(  ### Marker für jede Stellenanzeige auf der Karte
                                    location=[lat, lon],
                                    popup=folium.Popup(popup_html, max_width=250),
                                    icon=folium.Icon(color="blue", icon="briefcase", prefix="fa")
                                ).add_to(job_map)

                        # Streamlit-Anzeige
                        st_folium(job_map, width=700, height=500)
                    else:
                        st.warning("Keine Koordinaten für die Karte verfügbar.")
            else:
                st.error(f"Fehler beim Abrufen der Daten: {response.status_code}")