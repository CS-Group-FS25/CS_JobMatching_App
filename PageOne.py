import streamlit as st 
import pandas as pd
 
import streamlit as st
import requests

def datenabfrage(): 
    import streamlit as st 
    import pandas as pd
 
    import streamlit as st
    import requests

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
    Ort = st.text_input("In welcher Region suchst du?")
    Branche = st.multiselect("Welche Branche interessiert dich?", ["Finanzen", "Software", "Vertrieb", "Soziales", "Lehrer", "Baubranche", "Verwaltung"
                                                                       "Logistik"])
    Bildungsabschluss = st.radio("Hast du einen Bildungsabschluss?", ("Ja", "Nein"))
    if Bildungsabschluss == "Ja":
        Akademisches_Niveau = st.radio("Welche Ausbildung haben Sie?", ("Ausbildung", "Studium", ))    
    Berufserfahrung = st.selectbox("Wie viel Berufserfahrung haben Sie?", ("0-1 Jahr", "2-5 Jahre", "Mehr als 5 Jahre"))
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
        **Alter:** {profil.alter}"
        **Ort:** {profil.ort}"
        **Branche:** {profil.branche}"
        **Bildungsabschluss:** {profil.abschluss}"
        **Akademisches Niveau:** {profil.akademisches_niveau}"
        **Berufserfahrung:** {profil.berufserfahrung}"
        **Arbeitszeit:** {profil.arbeitszeit}"
        """)


# BA API Konfiguration
API_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
API_KEY = "jobboerse-jobsuche"  # Öffentlicher Key

# Jobsuche-Funktion bei der BA
def suche_jobs(beruf, ort, anzahl=10):
    headers = {
        "X-API-Key": API_KEY # Öffentlicher Key
    }
    #Suchparameter
    params = {
        "was": beruf,
        "wo": ort,
        "size": anzahl
    }
    #API Anfrage
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("stellenangebote", []) # Wiedergabe der Stellenangebote
    else:
        st.error(f"Fehler bei der API-Anfrage: {response.status_code}")
        return []

# Aufbau der Jobsuche 
def main():
    st.title("💼 Job-Suche mit der Bundesagentur für Arbeit")
    st.write("Nutze diese Suche, um passende Jobs in deiner Region zu finden.")

    beruf = st.text_input("Beruf / Stichwort", "Softwareentwickler")
    ort = st.text_input("Ort", "Berlin")
    anzahl = st.slider("Anzahl der Ergebnisse", 1, 50, 10)

    if st.button("🔍 Suche starten"):
        with st.spinner("Lade Ergebnisse..."):
            jobs = suche_jobs(beruf, ort, anzahl)

        if jobs:
            st.success(f"{len(jobs)} Stellen gefunden:")
            for job in jobs:
                st.subheader(job.get("titel", "Kein Titel"))
                st.write(f"📍 {job.get('arbeitsort', {}).get('ort', 'Unbekannt')}")
                st.write(f"🗓️ Veröffentlicht: {job.get('veroeffentlichtAm', 'k.A.')}")
                link = job.get("stellenURL")
                if link:
                    st.markdown(f"[Zur Stellenanzeige]({link})", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.info("Keine Stellen gefunden. Bitte versuche andere Suchbegriffe.")

