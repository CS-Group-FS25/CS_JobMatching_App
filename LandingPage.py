import streamlit as st
import pandas as pd
import numpy as np
import requests
import PageOne
import PageTwo
import PageThree
import PageFour
import PageDashboardTest
import PageTestML

industry_df = None
industries = None
clustered_skills_df = None

def load_data():
    global industry_df, industries, clustered_skills_df
    if industry_df is None:
        industry_df = pd.read_parquet("DataHandling/cluster_industry_preview.parquet")
        industries = sorted(industry_df["industry"].dropna().unique())
    if clustered_skills_df is None:
        clustered_skills_df = pd.read_parquet("DataHandling/clustered_skills.parquet")

def main():
    st.set_page_config(page_title="Job Fit App", page_icon=":briefcase:", layout="wide")

    load_data() # Lade alle Dataframes welche die App benötigt

    ### session_state
    if 'page' not in st.session_state:
        st.session_state.page = 'Startseite'

    menü = st.sidebar.radio("Menu", ("Startseite", "Job Matcher", "Klassische Job-Suche", "Gehaltsfinder", "Über uns", "ML Test", "Dashboard Test"))

    if menü != "Startseite":
        st.session_state.page = menü

    if st.session_state.page == "Startseite":
        st.title("Job Fit App")
        st.subheader("Wilkommen zu deinem persönlichen Job Matcher")
        st.divider()
        st.markdown(
            """ 
            ## Intro
            Diese App ist eine Job-Matching-Anwendung, die Ihnen hilft, den perfekten Job zu finden.
            Sie können Ihre Fähigkeiten und Interessen eingeben, und die App wird Ihnen passende Stellenangebote vorschlagen.
            ### An der Seite können sie aus verschiedenen Funktionen wählen!
            Für weitere Jobs klicken sie auf die folgenden Links:
            - [LinkedIn](https://business.linkedin.com/de-de/talent-solutions)
            - [Step Stone](https://www.stepstone.de/)
            """
        )
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
    elif st.session_state.page == "Job Matcher":
        PageOne.main()
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
