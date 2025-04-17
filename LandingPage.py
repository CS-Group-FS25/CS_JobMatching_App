import streamlit as st

# Titel und Beschreibung
st.title("Job Matching Application")
st.subheader("Welcome to your personal Job Matcher")
st.write("Find the best job for you based on your preferences!")
st.write("Please choose your preferred function on the left sidebar:")

# Sidebar-Menü
menu = st.sidebar.radio("Menu", ("Startseite", "Job Matcher", "Job nach Region", "Gehaltsfinder", "About"))

# Inhalte je nach Menüpunkt anzeigen
if menu == "Startseite":
    st.write("Finde jetzt deinen Traumjob!")
    st.subheader("Schritt 1 - zeige uns deine Interessen")
    st.subheader("Schritt 2 - Zeige uns deine Stärken")
    st.subheader("Schritt 3 - Finde den Job, der zu dir passt!")
