import streamlit as st
import pandas as pd
import os
import toml
import PageOne
import PageDashboardTest
import PageTwo
import PageFour
import PageTestML
import PageThree
import joblib
import Dashboard
from streamlit.runtime.scriptrunner import get_script_run_ctx

st.set_page_config(page_title="Job Fit App", page_icon=":briefcase:", layout="wide")

st.markdown("""
    <style>
        /* Minimale Sidebar-Breite erzwingen */
        [data-testid="stSidebar"] {
            width: auto !important;
            min-width: unset !important;
            max-width: 280px !important;
            padding-right: 1rem;
        }

        /* Sidebar-Textfarbe */
        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Optional: aktives Element hervorheben */
        [data-testid="stSidebar"] .stRadio > div > label[data-selected="true"] {
            background-color: #0b9444 !important;
            border-radius: 5px;
        }

        /* Hauptinhalt links bündig halten */
        .main {
            margin-left: 220px;
        }
    </style>
""", unsafe_allow_html=True)

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

def get_theme_colors():
    config_path = os.path.join(".streamlit", "config.toml")
    if os.path.exists(config_path):
        config = toml.load(config_path)
        return config.get("theme", {})
    return {}

def main():
    # Lade Color Code von der Config Datei, damit Farbcodierung in manuellen st.markdown Objekten dem
    # allgemeinen in der config definierten Farbcode entsprechen
    if any(key not in st.session_state for key in ("primary_color", "bg_color", "sec_bg_color", "text_color")):
        theme = get_theme_colors()
        st.session_state.primary_color = theme.get("primaryColor", "#FF5733")
        st.session_state.bg_color = theme.get("backgroundColor", "#FFFFFF")
        st.session_state.sec_bg_color = theme.get("secondaryBackgroundColor", "#8F8F8F")
        st.session_state.text_color = theme.get("textColor", "#000000")

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
        st.markdown(f"""
            <div style="text-align: center; padding: 2rem 1rem;">
                <h1 style="font-size: 3rem;">🚀 Willkommen bei der Personal Job Fit App</h1>
                <p style="font-size: 1.3rem; color: darkgray;">Finde den Job, der wirklich zu dir passt – basierend auf deinen Skills, Interessen und Werten.</p>
            </div>
        """, unsafe_allow_html=True)
        st.divider()
        sec_bg = st.session_state.sec_bg_color
        st.markdown("""
        <style>
        a.card-link {
            text-decoration: none !important;
            color: inherit !important;
            display: block;
        }
        .feature-card {
            background-color: #f0f0f033;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid #77777733;
            transition: 0.3s;
            min-height: 260px;
        }
        .feature-card:hover {
            background-color: #ffffff10;
            border-color: #aaaaaa66;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            cursor: pointer;
        }
        .feature-card h3 {
            margin-bottom: 0.5rem;
        }
        .feature-card p {
            font-size: 0.9rem;
            color: #bbb;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
                <a href="/?page_redirect=Klassische Job-Suche" target="_self" class="card-link">
                    <div class="feature-card">
                        <h3>🔍</p>Klassische Suche</h3>
                        <p>Durchsuche den Markt nach Stellen in deiner Region.</p>
                    </div>
                </a>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <a href="/?page_redirect=Personal Job Matcher" target="_self" class="card-link">
                    <div class="feature-card">
                        <h3>🧠</p>Persönlicher Matcher</h3>
                        <p>Erhalte massgeschneiderte Jobvorschläge auf Basis deiner Skills.</p>
                    </div>
                </a>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <a href="/?page_redirect=Gehaltsfinder" target="_self" class="card-link">
                    <div class="feature-card">
                        <h3>💰</p>Gehaltsfinder</h3>
                        <p>Vergleiche, was andere in deiner Branche verdienen.</p>
                    </div>
                </a>
            """, unsafe_allow_html=True)

        # Query param auslesen (oben definierter redirect)
        if "page_redirect" in st.query_params:
            st.session_state.page_redirect = st.query_params["page_redirect"]
            st.query_params.clear()
            st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="text-align: center; padding: 2rem;">
                <h2 style="margin-bottom: 0.5rem;">Bereit, deinen Traumjob zu finden?</h2>
                <p style="font-size: 1.1rem; color: #bbb;">Starte jetzt durch mit dem Personal Job Matcher.</p>
                <a href="/?page_redirect=Personal Job Matcher" target="_self">
                    <button style="padding: 0.75rem 2rem; font-size: 1.1rem; background-color: #FF0000; color: white; border: none; border-radius: 8px; margin-top: 1rem;">🚀 Jetzt starten</button>
                </a>
            </div>
        """, unsafe_allow_html=True)

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
