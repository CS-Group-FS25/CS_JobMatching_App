import streamlit as st
import PageOne

# Initialisierung von session_state
if "seite" not in st.session_state:
    st.session_state.seite = "Startseite"
# Initialisierung von session_state.button, wir abgefragt ob ein button geclickt wurde
if "button" not in st.session_state: 
    st.session_state.button = False

#liste der verschiedenen Seiten
seiten = ["Startseite","Job Matcher",]

#Sidebar als selectbox (finde ich ästhetischer) mit der Liste der seiten oben
auswahl = st.sidebar.selectbox("Seite wählen", seiten)

#Falls kein button geclickt, st.sesison_state.seite auf die Auswahl der sidebar überschrieben werden
if st.session_state.button == False:
    st. session_state.seite = auswahl

#Falls button geclickt, st.session_state.seite nicht überschrieben werden
#Danach soll der st.session_state.button wieder auf False ändern damit man beim nächsten reload nicht stuck ist
elif st.session_state.button == True: #Neu
    st.session_state.button = False


# Startseite-Inhalte
if st.session_state.seite == "Startseite":
    st.title("Job Matching Application")
    st.subheader("Willkommen zu unserem Job Matcher!")
    st.write("Finde mit 3 einfachen Schritten zu deinem Traumjob!")
    st.subheader("Schritt 1 - Zeige uns deine Interessen")
    st.subheader("Schritt 2 - Zeige uns deine Stärken")
    st.subheader("Schritt 3 - Finde den Job, der zu dir passt!")
    
# Button denke ich selbsterklären, wichig ist dass der Aufbau für jeden Button beibehalten wird
    if st.button("Jetzt Loslegen"):
        st.session_state.seite = "Job Matcher" 
        st.session_state.button = True
        st.rerun()

# Job Matcher-Inhalte
elif st.session_state.seite == "Job Matcher":
    st.title("Willkommen beim Job Matcher")
    PageOne.api_google_jobs()
   
    
    # Button selbsterklären
    if st.button("Zurück zur Startseite"):
        st.session_state.seite = "Startseite"
        st.session_state.button = True
        st.rerun()

    
    
    
    
    

