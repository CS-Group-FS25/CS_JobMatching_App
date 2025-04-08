import streamlit as st

def landing_page():
    """Kommentar für Funktionen so formatieren. Dadurch kann das hier geschriebene
    auch mit help(laning_page) abgerufen werden.
    """
    st.title("Job Fit Application")
    st.subheader("Welcome to your personal Job Matcher")
    st.write("Find the best job for you based on your preferences!")
    st.write("Please chose your prefered function on the left sidebar:")

    menü = st.sidebar.radio("Menu", ("Startseite", "Job Matcher", "Job nach Region", "Gehaltsfinder", "About" ))
    if menü == "Startseite": 
        st.write("This is the Startseite page")

    if menü == "Job Matcher":
    
