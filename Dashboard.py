import streamlit as st
import requests
import folium
from streamlit import session_state
from streamlit_folium import st_folium
import statistics

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
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.job_titles_list[st.session_state.clicked_job].
                    upper()}</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1.8])

        # Left Column: Map and Job List
        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Job Möglichkeiten in deiner Region")
            run_job_search(st.session_state.job_titles_list[st.session_state.clicked_job],
                           st.session_state.profil.location)

        # Rechte Spalte: Tabs mit Salary Übersicht und Top 5 Job Übersicht
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["Gehaltsübersicht", "Top 5 Jobs"])

            # Salary Logik
            with tab1:
                # Lade df_salary, category, histogram_data falls main() von PageThree (Gehaltsfinder) noch nicht
                # ausgeführt wurde, da sonst df_salary nicht definiert ist
                if (
                    "df_salary" not in st.session_state 
                    or "category" not in st.session_state
                    or st.session_state.category != st.session_state.profil.branche
                    ):
                    df_salary, category = PageThree.datenverarbeitung(st.session_state.profil.branche)
                    st.session_state.df_salary = df_salary
                    st.session_state.category = category
                if (
                    "histogram_data" not in st.session_state
                    or st.session_state.category != st.session_state.profil.branche
                ):
                    st.session_state.histogram_data = PageThree.datenabfrage_verteilung(st.session_state.category)

                    st.markdown("""
                <div style="background-color: {bg}; padding: 20px 20px 10px 20px; border-radius: 10px;">
                    <h4 style="text-align: center;">📊 Gehaltsübersicht</h4>
                    <div style="display: flex; justify-content: space-between; gap: 40px;">
                        <div style="flex: 1;">
                            <p style="margin: 0;"><strong>💰 Gehalt zuletzt:</strong></p>
                            <span style='display: block; font-size: 1.8em; font-weight: bold; margin-top: 6px; margin-bottom: 0;'>{gehalt}</span>
                        </div>
                        <div style="flex: 1; text-align: right;">
                            <p style="margin: 0;"><strong>📈 Durchschnittsgehalt</strong></p>
                            <span style='display: block; font-size: 1.8em; font-weight: bold; margin-top: 6px; margin-bottom: 0;'>{avg_gehalt}</span>
                        </div>
                    </div>
                </div>
                """.format(
                    bg=st.session_state.sec_bg_color,
                    monat=st.session_state.df_salary["Monat"].max().strftime("%B %Y"),
                    gehalt=f"{st.session_state.df_salary['Durchschnittsgehalt'].iloc[-1]:,.0f} CHF".replace(",", "."),
                    avg_gehalt=f"{statistics.mean(st.session_state.df_salary['Durchschnittsgehalt']):,.0f} CHF".replace(
                        ",", ".")
                ), unsafe_allow_html=True)

                PageThree.gehaltsdiagramm(session_state.df_salary,
                                          st.session_state.profil.branche,
                                          False,
                                          True)
                PageThree.zeige_gehaltshistogramm(st.session_state.histogram_data, True)

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