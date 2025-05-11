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

if "industry_df" not in st.session_state:
    st.session_state.industry_df = pd.read_parquet("DataHandling/cluster_industry_preview.parquet")
    st.session_state.industries = sorted(st.session_state.industry_df["industry"].dropna().unique())
if "clustered_skills_df" not in st.session_state:
    st.session_state.clustered_skills_df = pd.read_parquet("DataHandling/clustered_skills.parquet")
if "model" not in st.session_state or "industry_encoder" not in st.session_state:
    st.session_state.model, st.session_state.industry_encoder = (
        joblib.load("DataHandling/trained_random_forest_with_industry.pkl"))
if "clicked_job" not in st.session_state:
    st.session_state.clicked_job = None

def main():
    ### session_state
    if 'page' not in st.session_state:
        st.session_state.page = 'Startseite'

    if "page_redirect" in st.session_state:
        st.session_state.page = st.session_state.page_redirect
        del st.session_state.page_redirect

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
        key="page"
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
            if st.button('Personal Job Matcher'):
                st.session_state.page_redirect = "Personal Job Matcher"
                st.rerun()
        with col2:
            if st.button('Klassische Job-Suche'):
                st.session_state.page_redirect = "Klassische Job-Suche"
                st.rerun()
        with col3:
            if st.button('Gehaltsfinder'):
                st.session_state.page_redirect = "Gehaltsfinder"
                st.rerun()


    # Menü Bedienung
    elif st.session_state.page == "Personal Job Matcher":
        PageOne.main()
    elif st.session_state.page == "Job Dashboard":
        Dashboard.main()
    elif st.session_state.page == "Klassische Job-Suche":
        PageTwo.main()
    elif st.session_state.page == "Gehaltsfinder":
        PageThree.main()
    elif st.session_state.page == "Über uns":
        PageFour.main()
    elif st.session_state.page == "ML Test":
        PageTestML.main()
    elif st.session_state.page == "Dashboard Test":
        PageDashboardTest.main()


main()
