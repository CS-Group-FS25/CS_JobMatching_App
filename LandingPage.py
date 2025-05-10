import streamlit as st
import pandas as pd
import PageOne
import PageDashboardTest
import PageTwo
import PageFour
import PageTestML
import PageThree
import joblib
import Dashboard

st.set_page_config(page_title="Job Fit App", page_icon=":briefcase:", layout="wide")

industry_df = None
industries = None
clustered_skills_df = None      # DIESE LOGIK NOCH ÄNDERN DAMIT SIE DURCH DEN RERUN IN PAGEONE NICHT ALLE NEUGELADEN WERDEN (SIEHE BILD, mit Session State!!!)
model = None
industry_encoder = None


def load_data():
    global industry_df, industries, clustered_skills_df, model, industry_encoder
    if industry_df is None:
        industry_df = pd.read_parquet("DataHandling/cluster_industry_preview.parquet")
        industries = sorted(industry_df["industry"].dropna().unique())
    if clustered_skills_df is None:
        clustered_skills_df = pd.read_parquet("DataHandling/clustered_skills.parquet")
    if model is None or industry_encoder is None:
        model, industry_encoder = joblib.load("DataHandling/trained_random_forest_with_industry.pkl")

def main():
    load_data() # Lade alle Dataframes welche die App benötigt

    ### session_state
    if 'page' not in st.session_state:
        st.session_state.page = 'Startseite'

    menu = st.sidebar.radio(
        "Menu",
        (
            "Startseite",
            "Personal Job Matcher",
            "Job Dashboard",
            "Klassische Job-Suche",
            "Gehaltsfinder",
            "Über uns",
            "ML Test",
            "Dashboard Test"
        ),
        index=(
            ["Startseite", "Personal Job Matcher", "Job Dashboard", "Klassische Job-Suche", "Gehaltsfinder",
                  "Über uns", "ML Test", "Dashboard Test"].index(st.session_state.page)
        )
    )

    if menu != st.session_state.page:
        st.session_state.page = menu

    if st.session_state.page == "Startseite":
        st.title("Job Fit App")
        st.subheader("Wilkommen zu deinem persönlichen Job Matcher")
        st.divider()
        st.markdown(
            """ 
            ## Intro
            Diese App ist eine Job-Matching-Anwendung, die Ihnen hilft, den perfekten Job zu finden.
            Sie können Ihre Fähigkeiten und Interessen eingeben, und die App wird Ihnen passende Stellenangebote vorschlagen.
            """
        )
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('JobMatcher'):
                st.session_state.page = "Job Matcher"
                PageOne.main()
        with col2:
            if st.button('Klassische Job-Suche'):
                st.session_state.page = "Klassische Job-Suche"
                PageTwo.main()
        with col3:
            if st.button('Gehaltsfinder'):
                st.session_state.page = "Gehaltsfinder"
                PageThree.main()


    # Menü Bedienung
    elif st.session_state.page == "Personal Job Matcher":
        PageOne.main()
    elif st.session_state.page == "Job Dashboard":
        Dashboard.main()
    elif st.session_state.page == "Klassische Job-Suche":
        PageTwo.main()
    elif st.session_state.page == "Gehaltsfinder":
        PageThree.main()
    elif st.session_state.page == "Über Uns":
        PageFour.main()
    elif st.session_state.page == "ML Test":
        PageTestML.main()
    elif st.session_state.page == "Dashboard Test":
        PageDashboardTest.main()


main()
