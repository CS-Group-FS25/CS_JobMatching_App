import streamlit as st
import pandas as pd
import requests
import LandingPage
import SkillCategories

### Benutzprofil als Klasse definieren
class Benutzerprofil:
    def __init__(self, alter, ort, branche, abschluss, akademisches_niveau, berufserfahrung, arbeitszeit, skills):
        self.alter = alter
        self.ort = ort
        self.branche = branche
        self.abschluss = abschluss
        self.akademisches_niveau = akademisches_niveau
        self.berufserfahrung = berufserfahrung
        self.arbeitszeit = arbeitszeit
        self.skills = skills

def styled_multiselect(label, options, key):
    st.markdown(f"<div style='min-height: 3em'><strong>{label}</strong></div>", unsafe_allow_html=True)
    return st.multiselect("", options, key=key)

### Funktion der Profilerstellung und der Datenabfrage
def datenabfrage():
    ### Willkommen + Abfrage der Daten
    st.title("Dein Persönlicher Job-Matcher")
    st.header("Kreiere zuerst dein persönliches Profil")

    Alter = st.text_input("Bitte gebe dein Alter ein")
    Ort = st.text_input("In welcher Region suchst du nach einem Job?")
    Branche = st.selectbox("In welcher Branche möchtest Du arbeiten?", LandingPage.industries)
    Bildungsabschluss = st.radio("Hast du einen Bildungsabschluss?", options=("Ja", "Nein"), horizontal=True)
    if Bildungsabschluss == "Ja":
        Akademisches_Niveau = st.radio("Welche Ausbildung haben Sie?", ("Schulabschluss", "Ausbildung", "Studium",))
    Berufserfahrung = st.selectbox("Wie viel Berufserfahrung haben Sie?",
                                   ("Keine Erfahrung", "0-1 Jahr", "2-5 Jahre", "Mehr als 5 Jahre"))
    Arbeitszeit = st.selectbox("Wie viel Zeit kannst du investieren?", ("Vollzeit", "Teilzeit", "Minijob"))

    st.write("Wähle deine Skills aus:")
    cols = st.columns(5)    # Erstellung von 5 Spalten für die Dropdown Menüs der Skills
    category_names = list(SkillCategories.skill_categories.keys())

    selected_skills_by_cat = {}

    # Zeile 1 von den Skill Auswahlfeldern
    cols_row1 = st.columns(5)
    for i in range(5):
        cat = category_names[i]
        with cols_row1[i]:
            selected = styled_multiselect(cat, SkillCategories.skill_categories[cat], key=cat)
            if selected:
                selected_skills_by_cat[cat] = selected

    # Zeile 2 von den Skill Auswahlfeldern
    cols_row2 = st.columns(5)
    for i in range(5, 10):
        cat = category_names[i]
        with cols_row2[i - 5]:
            selected = styled_multiselect(cat, SkillCategories.skill_categories[cat], key=cat)
            if selected:
                selected_skills_by_cat[cat] = selected

    ### aktuelles Profil speichern
    profil = Benutzerprofil(
        alter=Alter,
        ort=Ort,
        branche=Branche,
        abschluss=Bildungsabschluss,
        akademisches_niveau=Akademisches_Niveau,
        berufserfahrung=Berufserfahrung,
        arbeitszeit=Arbeitszeit,
        skills = selected_skills_by_cat
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
        **SKills:** {profil.skills}
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
        'where': profil.ort  # Region (richtig benannt)
    }

    # Adzuna API anfragen über requests
    response = requests.get(url, params=parameter)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        job_daten = response.json()

        ### Überprüfen, ob Jobs gefunden werden
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
    profil = datenabfrage()
    job_title = st.text_input("🔧 Stichwort (z. B. Python Entwickler)", "python")
    if st.button("Job suchen"):
        if job_title:
            job_suchen(job_title, profil)
        else:
            st.warning("Kein Jobtitel")