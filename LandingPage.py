import streamlit as st

# Initialisierung von session_state
if "seite" not in st.session_state:
    st.session_state.seite = "Startseite"

seiten = ["Startseite","Job Matcher",]

auswahl = st.sidebar.selectbox("Seite wählen", seiten)

# Startseite-Inhalte
if st.session_state.seite == "Startseite":
    st.title("Job Matching Application")
    st.subheader("Willkommen zu unserem Job Matcher!")
    st.write("Finde mit 3 einfachen Schritten zu deinem Traumjob!")
    st.subheader("Schritt 1 - Zeige uns deine Interessen")
    st.subheader("Schritt 2 - Zeige uns deine Stärken")
    st.subheader("Schritt 3 - Finde den Job, der zu dir passt!")
    
    if st.button("Jetzt Loslegen"):
        st.session_state.seite = "Job Matcher" #Hier weiterhin das Problem, dass es einen Doppelclick
        #benötigt um die Seite neu zu laden
        st.rerun()

# Job Matcher-Inhalte
elif st.session_state.seite == "Job Matcher":
    st.title("Willkommen beim Job Matcher")
    
    if st.sidebar.button("Zurück zur Startseite"):
        st.session_state.seite = "Startseite"
        st.rerun()
    
    
    
    

