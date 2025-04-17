import streamlit as st

# Titel und Beschreibung


# Sidebar-Menü
menu = st.sidebar.radio("Menu", ("Startseite", "Zum Job Matcher", "Job nach Region", "Gehaltsfinder", "About"))

# Inhalte auf der Startseite
if menu == "Startseite":
    st.title("Job Matching Application")
    st.subheader("Willkommen zu unserem Job matcher!")
    st.write("Finde mit 3 einfachen Schritten zu deinem Traumjob!")
    st.subheader("Schritt 1 - zeige uns deine Interessen")
    st.subheader("Schritt 2 - Zeige uns deine Stärken")
    st.subheader("Schritt 3 - Finde den Job, der zu dir passt!")
    st.button("Jetzt Loslegen")
    if st.button("Jetzt Loslegen"):
        st.session_state.page = "Zum Job Matcher"

