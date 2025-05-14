import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

#Für das Beheben von Bugs wurde ChatGPt zur hilfe genommen

# Adzuna API Einrichten mit API ID und Schlüssel
APP_ID = "42d55acf"
APP_KEY = "2fde9c1ff58d9bfdf254dd3f0c4d6ec7"
url = f'https://api.adzuna.com/v1/api/jobs/ch/search/1'



def get_postcode_from_coords_or_name(job):
    #Funktion für Reverse-Geocoding
    ort = job["location"].get("display_name")
    if ort:  # Wenn ein Ort ausgegeben wird, wird die Plz gesucht und ausgegeben
        nominatim_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": ort,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        headers = {"User-Agent": "streamlit-job-app"}
        plz = requests.get(url, params=params, headers=headers)
        if plz.status_code == 200 and plz.json():  # Bei erfolgreicher Abfrage wird die PLZ zurückgegeben
            data = plz.json()[0] # speichern der Antwort in einer Variablen
            return data.get("address", {}).get("postcode", "PLZ nicht gefunden")
    return "PLZ nicht verfügbar" 


def main():
    st.title("🔍 Klassische Jobsuche") 
    st.markdown("Suche nach aktuellen Stellenanzeigen in der Schweiz.")

    # Eingabefelder für die Jobsuche
    # Nach Stichwort oder Jobtitel suchen
    job_title = st.text_input("🔧 Stichwort (z. B. Finanzen)", "Finanzen")
    location = st.text_input("📍 Ort (z. B. Zürich)", "Zürich")
    results_per_page = st.slider("📄 Anzahl der Ergebnisse", min_value=1, max_value=20, value=5)

    # Einrichten von Session_State
    if "suche_gestartet" not in st.session_state:
        st.session_state["suche_gestartet"] = False

    # Button zum Auslösen der Suche
    if st.button("🔎 Jobs suchen"):
        st.session_state["suche_gestartet"] = True

    if st.button("🔄 Neue Suche starten"):
        st.session_state["suche_gestartet"] = False
        st.rerun()

    # Wenn die Suche gestartet wurde, wird die API aufgerufen
    if st.session_state["suche_gestartet"]:
        with st.spinner("Suche läuft..."):
            # notwendige Parameter für die API-Abfrage
            params = {
                'app_id': APP_ID,
                'app_key': APP_KEY,
                'what': job_title,
                'where': location,
                'results_per_page': results_per_page,
                'content-type': 'application/json'
            }
            # Speichern der Antwort in einer Variablen
            response = requests.get(url, params=params)
            
            # Wenn die API erfolgreich abgerufen wurde, wird die Antwort verarbeitet    
            if response.status_code == 200:  

                data = response.json() # Json Daten
                results = data.get("results", [])
                if not results:
                    st.info("Keine Jobs gefunden.")

                map_data = []
                column1, column2 = st.columns(2)
                with column1:  # Spalte 1 mit Darstellung der Jobanzeigen
                    for job in results:
                        st.subheader(job.get("title"))
                        st.write("📌 Firma:", job.get("company", {}).get("display_name", "Unbekannt"))
                        st.write("📍 Ort:", job.get("location", {}).get("display_name", ""))
                        longitude = job.get("longitude")  # Wichtige Koordinaten für die Karte
                        latitude = job.get("latitude")
                        st.write("🌍 Koordinaten:", f"({latitude}, {longitude})")
                         # Falls die Stellenanzeige Koordinaten ausgibt, werden diese für die Karte gespeichert
                        if latitude is not None and longitude is not None:  
                            map_data.append({"lat": latitude, "lon": longitude})

                        st.write(job.get("description", "")[:300] + "...")
                        st.markdown(f"[🔗 Zum Job]({job.get('redirect_url')})")

                    # PLz ausgeben
                    Postleitzahl = get_postcode_from_coords_or_name(job)
                    st.write("📮 PLZ:", Postleitzahl)
                with column2:  # Spalte 2 mit Darstellung der Karte
                    if map_data:
                        st.title(" Interaktive Karte")
                        # Für die Darstellung der Karte wurde ChatGPT zur Hilfe genommen
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
                            
                            # Wenn es Daten für die Karte gibt, werden diese angezeigt
                            
                            if lat and lon:
                                popup_html = f"<b>{title}</b><br>{company}<br><a href='{url}' target='_blank'>Zum Job</a>"
                                folium.Marker(  # Marker für jede Stellenanzeige auf der Karte
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