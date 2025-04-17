import streamlit as st

# Initialisierung von session_state
if "seite" not in st.session_state:
    st.session_state.seite = "Startseite"

# Seitenoptionen
seiten = ("Startseite", "Job Matcher", "About")

# Nur Sidebar-Menü anzeigen, wenn NICHT durch Button-Navigation gesteuert wurde
if st.session_state.seite in seiten:
    menu = st.sidebar.radio("Menu", seiten, index=seiten.index(st.session_state.seite))
    st.session_state.seite = menu  # Menüauswahl auch in session_state schreiben
else:
    menu = st.session_state.seite

# Startseite-Inhalte
if st.session_state.seite == "Startseite":
    st.title("Job Matching Application")
    st.subheader("Willkommen zu unserem Job Matcher!")
    st.write("Finde mit 3 einfachen Schritten zu deinem Traumjob!")
    st.subheader("Schritt 1 - Zeige uns deine Interessen")
    st.subheader("Schritt 2 - Zeige uns deine Stärken")
    st.subheader("Schritt 3 - Finde den Job, der zu dir passt!")
    
    if st.button("Jetzt Loslegen"):
        st.session_state.seite = "Job Matcher"

# Job Matcher-Inhalte
elif st.session_state.seite == "Job Matcher":
    st.title("Willkommen beim Job Matcher")
    
    if st.sidebar.button("Zurück zur Startseite"):
        st.session_state.seite = "Startseite"
    
    
    
    

