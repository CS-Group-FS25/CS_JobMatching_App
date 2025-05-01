import streamlit as st
import requests

def main():
    # Adzuna API Einrichten mit API ID und Schlüssel
    APP_ID = "42d55acf"
    APP_KEY = "2fde9c1ff58d9bfdf254dd3f0c4d6ec7"

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
                    st.markdown("---")
            else:
                st.error(f"Fehler beim Abrufen der Daten: {response.status_code}")


