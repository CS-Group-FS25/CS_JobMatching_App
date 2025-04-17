import streamlit as st

#Setzten von session_state.seite (Speichert die Seite zwischen reloads damit Buttons funktionieren)
if "seite" not in st.session_state:
    st.session_state.seite = "Startseite"

# Sidebar-Menü
menu = st.sidebar.radio("Menu", ("Startseite", "Job Matcher", "Job nach Region", "Gehaltsfinder", "About"), index=("Startseite", "Job Matcher", "Job nach Region", "Gehaltsfinder", "About").index(st.session_state.seite))

# Inhalte auf der Startseite
if menu == "Startseite":
    st.title("Job Matching Application")
    st.subheader("Willkommen zu unserem Job matcher!")
    st.write("Finde mit 3 einfachen Schritten zu deinem Traumjob!")
    st.subheader("Schritt 1 - zeige uns deine Interessen")
    st.subheader("Schritt 2 - Zeige uns deine Stärken")
    st.subheader("Schritt 3 - Finde den Job, der zu dir passt!")
    if st.button("Jetzt Loslegen"):
        st.session_state.seite = "Job Matcher"
if menu == "Job Matcher":
    st.title("Willkommen beim Job Matcher")
    if st.sidebar.button("Zurück zur Landingpage"):
        st.session_state.seite = "Startseite"

    
    
    
    

