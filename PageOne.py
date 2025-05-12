import ast
import streamlit as st
import pandas as pd
import requests
import Dashboard
import SkillCategories
import numpy as np
import altair as alt


### Benutzprofil als Klasse definieren
class Benutzerprofil:
    def __init__(self, alter, location, branche, abschluss, akademisches_niveau, berufserfahrung, arbeitszeit, skills):
        self.alter = alter
        self.location = location
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
    st.title("Dein Persönlicher JobMatcher")
    st.header("Kreiere zuerst dein persönliches Profil")

    Alter = st.text_input("Bitte gebe dein Alter ein")
    Location = st.text_input("In welcher Region suchst du nach einem Job?")
    Branche = st.selectbox("In welcher Branche möchtest Du arbeiten?", st.session_state.industries)
    Bildungsabschluss = st.radio("Hast du einen Bildungsabschluss?", options=("Ja", "Nein"), horizontal=True)
    if Bildungsabschluss == "Ja":
        Akademisches_Niveau = st.radio("Welche Ausbildung haben Sie?", ("Schulabschluss", "Ausbildung", "Studium",))
    Berufserfahrung = st.selectbox("Wie viel Berufserfahrung haben Sie?",
                                   ("Keine Erfahrung", "0-1 Jahr", "2-5 Jahre", "Mehr als 5 Jahre"))
    Arbeitszeit = st.selectbox("Wie viel Zeit kannst du investieren?", ("Vollzeit", "Teilzeit", "Minijob"))

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("Wähle deine Skills aus:")
    cols = st.columns(5)  # Erstellung von 5 Spalten für die Dropdown Menüs der Skills
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

    st.markdown("<hr style='height:2px;border:none;color:#333;background-color:#333;'>", unsafe_allow_html=True)

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
        location=Location,
        branche=Branche,
        abschluss=Bildungsabschluss,
        akademisches_niveau=Akademisches_Niveau,
        berufserfahrung=Berufserfahrung,
        arbeitszeit=Arbeitszeit,
        skills=selected_skills_by_cat
    )

    ### Profil anzeigen unterhalb der Eingabefelder
    with st.expander("Profil anzeigen"):
        st.markdown(f"""
        **Alter:** {profil.alter}
        **Ort:** {profil.location}
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
    url = f'https://api.adzuna.com/v1/api/jobs/ch/search/1'  # Adzuna API für die Schweiz

    # Notwendige Eingaben für die Suche
    parameter = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'what': job_title,  # Jobtitel (richtig benannt)
        'where': profil.location  # Region (richtig benannt)
    }

    # Adzuna API anfragen über requests
    response = requests.get(url, params=parameter)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        job_daten = response.json()

        ### Überprüfen, ob Jobs gefunden werden
        if job_daten['results']:
            st.write(f"Gefundene Jobs in {profil.location} für {job_title}:")
            for job in job_daten['results']:  # Ändere 'jobs' zu 'job'
                title = job.get('title', 'Kein Titel verfügbar')
                company = job.get('company', {}).get('display_name', 'Unbekannt')
                location = job.get('location', {}).get('area', 'Unbekannt')
                url = job.get('redirect_url', '#')

                st.write(f"- **{title}** bei {company}, {location}")
                st.write(f"[Details anzeigen]({url})")
                st.write("\n")
        else:
            st.write(f"Keine Jobs für {job_title} in {profil.location} gefunden.")
    else:
        st.write(f"Fehler bei der API-Anfrage: {response.status_code}")


def predict_job(selected_skills, branche):
    # Suche die Cluster IDs der ausgewählten Skills aus Dataframe und speicher diese in einer Liste
    matched_clusters = st.session_state.clustered_skills_df[st.session_state.clustered_skills_df["skill"]
    .isin(selected_skills)]["cluster"].unique().tolist()

    # Alle 150 Cluster IDs sortiert
    all_clusters = sorted(st.session_state.clustered_skills_df["cluster"].unique())
    # Erstellung binären Vektors gemäss von Nutzer ausgewählten Skills
    feature_vector = [1 if cluster in matched_clusters else 0 for cluster in all_clusters]

    industry_df = pd.DataFrame([[branche]], columns=["industry"])
    # Von Nutzer ausgewählte Branche wird als One-Hot-Vektor dargestellt
    industry_onehot = st.session_state.industry_encoder.transform(industry_df)[0]

    # Verknüpfung von Skill-Vektor mit Branchen-Vektor
    x_input = np.array(feature_vector + list(industry_onehot)).reshape(1, -1)

    # Das trainierte Model gibt das wahrscheinlichste der 500 Job Cluster für den User zurück
    predicted_job_cluster = st.session_state.model.predict(x_input)[0]

    return representative_job_list(predicted_job_cluster)


def representative_job_list(predicted_job_cluster):
    job_cluster_row = st.session_state.industry_df[
        st.session_state.industry_df[
            "cluster_id"] == predicted_job_cluster]  # Es werden die zum vorhergesagten Job Cluster passende Zeile aus dem Dataframe ausgewählt

    if not job_cluster_row.empty:
        job_titles_str = job_cluster_row["example_titles"].values[
            0]  # Die Liste mit den 5 häufigsten Jobs des ausgewählten Job Clusters wird gespeichert
        job_titles_list = ast.literal_eval(job_titles_str)  # Umwandlung des Strings in eine Python Liste
        return job_titles_list
    else:
        st.warning("Das vorhergesagte Job Cluster beinhaltet keine Jobs.")
        return None


# Aufbau der Jobsuche
def main():
    st.session_state.profil = datenabfrage()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Finde Deine Top 5 Jobs</h3>", unsafe_allow_html=True)
    center_col = st.columns([6, 3, 6])[1]
    with center_col:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        clicked = st.button("🔍 Suche starten")
        st.markdown("</div>", unsafe_allow_html=True)

    # LOGIK NACH BUTTON-CLICK
    if clicked:
        selected_skills = [skill for skills in st.session_state.profil.skills.values() for skill in
                           skills]  # Speichere das Dictionary selected_skills_by_cat in eine flache Liste

        if not selected_skills or not st.session_state.profil.branche:
            st.warning("Bitte wähle mindestens einen Skill und die Branche aus.")
        else:
            job_titles_list = predict_job(selected_skills, st.session_state.profil.branche)
            st.session_state.job_titles_list = job_titles_list

    if "job_titles_list" in st.session_state:
        st.markdown("<hr style='height:2px;border:none;color:#333;background-color:#333;'>",
                    unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><h3>DEINE TOP 5 JOBS</h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><h5>Klicke auf einen Job für weitere Details</h5></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        jobs = st.session_state.job_titles_list[-5:]
        heights = [200, 140, 90, 60, 30]  # Beispiel-Höhen für Balken
        max_height = max(heights) + 40

        sorted_indices = np.argsort(heights)[::-1]
        medals = {sorted_indices[0]: "🥇", sorted_indices[1]: "🥈", sorted_indices[2]: "🥉"}

        cols = st.columns(5)

        for i, col in enumerate(cols):
            with col:
                # Balken mit Medaillen
                medal_html = ""
                if i in medals:
                    offset = max_height - heights[i] - 30
                    medal_html = f'<div style="position:absolute; top:{offset}px; font-size:24px;">{medals[i]}</div>'

                # HTML für Balken
                html_block = f"""
                    <div style="height:{max_height}px; position:relative; display:flex; flex-direction: column; justify-content:flex-end; align-items:center;">
                        {medal_html}  <!-- Medaille wird oben auf den Balken gesetzt -->
                        <div style="width:80%; height:{heights[i]}px; background-color:#098439; border-radius:10px; border:2px solid black;"></div>
                    </div>
                """
                st.markdown(html_block, unsafe_allow_html=True)

                # Button unter dem Balken
                button_style = """
                    <style>
                        div[data-testid="stButton"] {
                            display: flex;
                            justify-content: center;
                        }
                    </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)
                if st.button(f"{jobs[i]}", key=f"job_button_{i}"):
                    st.session_state.page_redirect = "Job Dashboard"
                    st.session_state.clicked_job = i
                    st.rerun()