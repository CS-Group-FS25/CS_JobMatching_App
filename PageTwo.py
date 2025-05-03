import streamlit as st
import requests

def main():
    # Adzuna API Einrichten mit API ID und Schlüssel
    APP_ID = "42d55acf"
    APP_KEY = "2fde9c1ff58d9bfdf254dd3f0c4d6ec7"
    # 🔁 Funktion für Reverse-Geocoding (OpenStreetMap / Nominatim)
    
    ### Versuch Plz zu lokalisieren
    def get_postcode_from_coords_or_name(job):
        lat = job["location"].get("latitude")
        lon = job["location"].get("longitude")

        ort = job["location"].get("display_name")
        if ort:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": ort,
                "format": "json",
                "addressdetails": 1,
                "limit": 1
            }
            headers = {"User-Agent": "streamlit-job-app"}
            r = requests.get(url, params=params, headers=headers)
            if r.status_code == 200 and r.json():
                data = r.json()[0]
                return data.get("address", {}).get("postcode", "PLZ nicht gefunden")
        return "PLZ nicht verfügbar"

    st.title("🔍 Klassische Jobsuche")
    st.markdown("Suche nach aktuellen Stellenanzeigen in der Schweiz.")

    # Eingabefelder
    job_title = st.text_input("🔧 Stichwort (z. B. Python Entwickler)", "python")
    location = st.text_input("📍 Ort (z. B. Zürich)", "Zürich")
    results_per_page = st.slider("📄 Anzahl der Ergebnisse", min_value=1, max_value=20, value=5)
    url = f'https://api.adzuna.com/v1/api/jobs/ch/search/1'
    # Button zum Auslösen der Suche
    if st.button("🔎 Jobs suchen"):
        with st.spinner("Suche läuft..."):
            params = {
                'app_id': APP_ID,
                'app_key': APP_KEY,
                'what': job_title,
                'where': location,
                'results_per_page': results_per_page,
                'content-type': 'application/json'
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if not results:
                    st.info("Keine Jobs gefunden.")
                for job in results:
                    st.subheader(job.get("title"))
                    st.write("📌 Firma:", job.get("company", {}).get("display_name", "Unbekannt"))
                    st.write("📍 Ort:", job.get("location", {}).get("display_name", ""))
                    st.write(job.get("description", "")[:300] + "...")
                    st.markdown(f"[🔗 Zum Job]({job.get('redirect_url')})")
                    
                    ### PLz filtern    
                    plz = get_postcode_from_coords_or_name(job)
                    st.write("📮 PLZ:", plz)
                    

            else:
                st.error(f"Fehler beim Abrufen der Daten: {response.status_code}")
    
    
    if st.button("Zurück zur Startseite"):
        st.session_state.seite = "Startseite"
        st.session_state.button = True
        import LandingPage
        LandingPage.main()
        
        
    

