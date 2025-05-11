import streamlit as st
import streamlit.components.v1 as components
import requests
import folium
from streamlit import session_state
from streamlit_folium import st_folium
import PageThree

# Adzuna API Einrichten mit API ID und Schlüssel
APP_ID = "42d55acf"
APP_KEY = "2fde9c1ff58d9bfdf254dd3f0c4d6ec7"
url = f'https://api.adzuna.com/v1/api/jobs/ch/search/1'

def run_job_search(job_title, location, results_per_page=10):
    #if st.session_state["suche_gestartet"]:
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
            for job in results:
                # Koordinaten für die Karte
                longitude = job.get("longitude")
                latitude = job.get("latitude")
                if latitude is not None and longitude is not None:  ### Falls die Stellenanzeige Koordinaten ausgibt, werden diese für die Karte gespeichert
                    map_data.append({"lat": latitude, "lon": longitude})

            if map_data:
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

                for job in results:
                    st.subheader(job.get("title"))
                    st.write("📌 Firma:", job.get("company", {}).get("display_name", "Unbekannt"))
                    st.write("📍 Ort:", job.get("location", {}).get("display_name", ""))
                    st.write("🌍 Koordinaten:", f"({latitude}, {longitude})")

                    st.write(job.get("description", "")[:300] + "...")
                    st.markdown(f"[🔗 Zum Job]({job.get('redirect_url')})")

            else:
                st.warning("Keine Koordinaten für die Karte verfügbar.")
        else:
            st.error(f"Fehler beim Abrufen der Daten: {response.status_code}")

def main():
    if st.session_state.clicked_job is not None:
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.job_titles_list[st.session_state.clicked_job].upper()}</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1.5])

        # Left Column: Map and Job List
        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Job Möglichkeiten in deiner Region")
            run_job_search(st.session_state.job_titles_list[st.session_state.clicked_job],
                           st.session_state.profil.ort)

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["Salary Range", "Top 5 Jobs"])

            with tab1:
                st.markdown("### Salary Range")
                PageThree.Gehaltsdiagramm(session_state.df_salary, st.session_state.profil.branche)

                components.html("""
                            <div style='width:100%; height:300px; background-color:#f2f2f2; display:flex; align-items:center; justify-content:center;'>
                                [Salary Chart Placeholder]
                            </div>
                        """, height=300)

            with tab2:
                st.markdown("### Your Top 5 Jobs")
                for i in range(0, 5):
                    if i == st.session_state.clicked_job:
                        st.button(
                            f"{st.session_state.job_titles_list[i]}", type="primary")

                    else:
                        if st.button(f"{st.session_state.job_titles_list[i]}", type="secondary"):
                            st.session_state.clicked_job = i
                            st.rerun()

    else:
        st.title("DEIN JOB DASHBOARD")
        st.warning("Besuche erst den Personal Job Matcher damit dir hier Jobs angezeigt werden")