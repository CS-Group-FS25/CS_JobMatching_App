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
    st.header("Kreiere zuerst dein persöonliches Profil")
    
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
    with st.expander("Profil anzeigen"):
        st.markdown(f"""
        **Alter:** {profil.alter}
        **Ort:** {profil.ort}
        **Branche:** {profil.branche}
        **Bildungsabschluss:** {profil.abschluss}
        **Akademisches Niveau:** {profil.akademisches_niveau}
        **Berufserfahrung:** {profil.berufserfahrung}
        **Arbeitszeit:** {profil.arbeitszeit}
        """)
    return profil

# Adzuna API Einrichten mit API ID und Schlüssel
APP_ID = "42d55acf"
APP_KEY = "2fde9c1ff58d9bfdf254dd3f0c4d6ec7"

def job_suchen(job_title, profil):
    url = f'https://api.adzuna.com/v1/api/jobs/ch/search/1'  # Adzuna API für deutschland

    # Notwendige Eingaben für die Suche
    parameter = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'what': job_title,  # Jobtitel (richtig benannt)
        'where': profil.ort   # Region (richtig benannt)
    }

    # Adzuna API anfragen über requests
    response = requests.get(url, params=parameter)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        job_daten = response.json()

        # Überprüfen, ob Ergebnisse vorhanden sind
        if job_daten['results']:
            st.write(f"Gefundene Jobs in {profil.ort} für {job_title}:")
            for job in job_daten['results']:  # Ändere 'jobs' zu 'job'
                title = job.get('title', 'Kein Titel verfügbar')
                company = job.get('company', {}).get('display_name', 'Unbekannt')
                location = job.get('location', {}).get('area', 'Unbekannt')
                url = job.get('redirect_url', '#')

                st.write(f"- **{title}** bei {company}, {location}")
                st.write(f"[Details anzeigen]({url})")
                st.write("\n")
        else:
            st.write(f"Keine Jobs für {job_title} in {profil.ort} gefunden.")
    else:
        st.write(f"Fehler bei der API-Anfrage: {response.status_code}")

    
# Aufbau der Jobsuche 
def main():
    datenabfrage()
    job_title = st.text_input("🔧 Stichwort (z. B. Python Entwickler)", "python")
    if st.button("Job suchen"):
        if job_title:
            job_suchen(job_title,profil)
        else:
            st.warning("Kein Jobtitel")    
        
    
    

    
