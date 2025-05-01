import streamlit as st 
import pandas as pd
import requests

def datenabfrage(): 
    ### Benutzerprofil Klasse erstellen

    class Benutzerprofil: 
        def __init__(self, alter, ort, branche, abschluss, akademisches_niveau, berufserfahrung, arbeitszeit):
            self.alter = alter
            self.ort = ort
            self.branche = branche
            self.abschluss = abschluss
            self.akademisches_niveau = akademisches_niveau
            self.berufserfahrung = berufserfahrung
            self.arbeitszeit = arbeitszeit

    ### Willkommen + Abfrage der Daten 
    st.title("Dein Persönlicher Job-Matcher")
    st.title("Kreiere zuerst dein persöonliches Profil")
    
    Alter = st.text_input("Bitte gebe dein Alter ein")
    Ort = st.text_input("In welcher Region suchst du nach einem Job?")
    Branche = st.multiselect("Welche Branche interessiert dich?(Mehrfachauswahl möglich)", ["Finanzen", "Software", "Vertrieb","Beratung", "Soziales", "Lehrer", "Baubranche", "Verwaltung"
                                                                       "Logistik", "Handel", "Industrie", "Pharma", "Dienstleistungen"])
    Bildungsabschluss = st.radio("Hast du einen Bildungsabschluss?", ("Ja", "Nein"))
    if Bildungsabschluss == "Ja":
        Akademisches_Niveau = st.radio("Welche Ausbildung haben Sie?", ("Schulabschluss", "Ausbildung", "Studium", ))    
    Berufserfahrung = st.selectbox("Wie viel Berufserfahrung haben Sie?", ("Keine Erfahrung", "0-1 Jahr", "2-5 Jahre", "Mehr als 5 Jahre"))
    Arbeitszeit = st.selectbox("Wie viel Zeit kannst du investieren?", ("Vollzeit", "Teilzeit", "Minijob"))


    ### aktuelles Profil speichern
    profil = Benutzerprofil(
        alter=Alter,
        ort=Ort,
        branche=Branche,
        abschluss=Bildungsabschluss,
        akademisches_niveau=Akademisches_Niveau,
        berufserfahrung=Berufserfahrung,
        arbeitszeit=Arbeitszeit   
    )

    ### Profil anzeigen unterhalb der Eingabefelder
    st.expander("Profil anzeigen")
    st.markdown(f"""
        **Alter:** {profil.alter}
        **Ort:** {profil.ort}
        **Branche:** {profil.branche}
        **Bildungsabschluss:** {profil.abschluss}
        **Akademisches Niveau:** {profil.akademisches_niveau}
        **Berufserfahrung:** {profil.berufserfahrung}
        **Arbeitszeit:** {profil.arbeitszeit}
        """)

# Adzuna API Einrichten mit API ID und Schlüssel
APP_ID = "42d55acf"
APP_KEY = "27ac7bac51f538681d1cf3fe57d8ae3e"

def job_suchen(job_title, region):
    url = f'https://api.adzuna.com/v1/jobs/ch/search/1'  # Adzuna API für die Schweiz

    # Notwendige Eingaben für die Suche
    parameter = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'what': job_title,  # Jobtitel (richtig benannt)
        'where': region   # Region (richtig benannt)
    }

    # Adzuna API anfragen über requests
    response = requests.get(url, params=parameter)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        job_daten = response.json()

        # Überprüfen, ob Ergebnisse vorhanden sind
        if job_daten['results']:
            st.write(f"Gefundene Jobs in {region} für {job_title}:")
            for job in job_daten['results']:  # Ändere 'jobs' zu 'job'
                title = job.get('title', 'Kein Titel verfügbar')
                company = job.get('company', {}).get('display_name', 'Unbekannt')
                location = job.get('location', {}).get('area', 'Unbekannt')
                url = job.get('redirect_url', '#')

                st.write(f"- **{title}** bei {company}, {location}")
                st.write(f"[Details anzeigen]({url})")
                st.write("\n")
        else:
            st.write(f"Keine Jobs für {job_title} in {region} gefunden.")
    else:
        st.write(f"Fehler bei der API-Anfrage: {response.status_code}")

    
# Aufbau der Jobsuche 
def main():
    datenabfrage()
    st.title("🔍 Adzuna Jobsuche")
    st.markdown("Suche nach aktuellen Stellenanzeigen in Deutschland.")

    # Eingabefelder
    job_title = st.text_input("🔧 Stichwort (z. B. Python Entwickler)", "python")
    location = st.text_input("📍 Ort (z. B. Berlin)", "Berlin")
    results_per_page = st.slider("📄 Anzahl der Ergebnisse", min_value=1, max_value=20, value=5)
    url = f'https://api.adzuna.com/v1/jobs/ch/search/1'
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

    
