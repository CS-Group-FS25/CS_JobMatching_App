import streamlit as st

# Titel und Beschreibung
st.title("Job Fit Application")
st.subheader("Welcome to your personal Job Matcher")
st.write("Find the best job for you based on your preferences!")
st.write("Please choose your preferred function on the left sidebar:")

# Sidebar-Menü
menu = st.sidebar.radio("Menu", ("Startseite", "Job Matcher", "Job nach Region", "Gehaltsfinder", "About"))

# Inhalte je nach Menüpunkt anzeigen
if menu == "Startseite":
    st.write("Du bist auf der Startseite.")
elif menu == "Job Matcher":
    st.write("Hier wird dein perfekter Job gefunden!")
elif menu == "Job nach Region":
    st.write("Hier kannst du Jobs nach Region filtern.")
elif menu == "Gehaltsfinder":
    st.write("Finde hier Informationen zu typischen Gehältern.")
elif menu == "About":
    st.write("Dieses Projekt wurde von Nicolas & Team erstellt.")