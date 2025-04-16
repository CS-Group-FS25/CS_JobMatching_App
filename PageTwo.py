import streamlit as st
import requests

# BA API Konfiguration
API_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
API_KEY = "jobboerse-jobsuche"  # Öffentlicher Key

def suche_jobs(beruf, ort, anzahl=10):
    headers = {
        "X-API-Key": API_KEY
    }
    params = {
        "was": beruf,
        "wo": ort,
        "size": anzahl
    }
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("stellenangebote", [])
    else:
        st.error(f"Fehler bei der API-Anfrage: {response.status_code}")
        return []

# Streamlit UI
st.title("💼 Job-Suche mit der Bundesagentur für Arbeit")
beruf = st.text_input("Beruf / Stichwort", "Softwareentwickler")
ort = st.text_input("Ort", "Berlin")
anzahl = st.slider("Anzahl der Ergebnisse", 1, 50, 10)

if st.button("🔍 Suche starten"):
    jobs = suche_jobs(beruf, ort, anzahl)
    if jobs:
        for job in jobs:
            st.subheader(job.get("titel", "Kein Titel"))
            st.write(f"📍 {job.get('arbeitsort', {}).get('ort', 'Unbekannt')}")
            st.write(f"🗓️ Veröffentlicht: {job.get('veroeffentlichtAm', 'k.A.')}")
            link = job.get("stellenURL")
            if link:
                st.markdown(f"[Zur Stellenanzeige]({link})", unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.info("Keine Stellen gefunden.")