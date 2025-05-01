import streamlit as st
import pandas as pd 
import numpy as np
import requests

st.set_page_config(page_title="Job Fit App", page_icon=":briefcase:", layout="wide")


menü = st.sidebar.radio("Menu", ("Startseite", "Job Matcher", "Klassische Job-Suche", "Gehaltsfinder", "Über uns"))
st.title("Job Fit App")
st.subheader("Wilkommen zu deinem persönlichen Job Matcher")
st.divider()

st.markdown(
    """ 
    ## Intro
    Diese App ist eine Job-Matching-Anwendung, die Ihnen hilft, den perfekten Job zu finden.
    Sie können Ihre Fähigkeiten und Interessen eingeben, und die App wird Ihnen passende Stellenangebote vorschlagen.
    ### An der Seite können sie aus verschiedenen Funktionen wählen!
    Für weitere Jobs klicken sie auf die folgenden Links:
    - [LinkedIn](https://business.linkedin.com/de-de/talent-solutions)
    - [Step Stone](https://www.stepstone.de/)
    """
)

# Setze default-Seite
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Navigation Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('JobMatcher'):
        st.session_state.page = 'page_one'
with col2:
    if st.button('Klassische Job-Suche'):
        st.session_state.page = 'page_two'
with col3:
    if st.button('Gehaltsfinder'):
        st.session_state.page = 'page_three'

# Seiten anzeigen
if st.session_state.page == 'page_one':
    import PageOne
    PageOne.main()
elif st.session_state.page == 'page_two':
    import PageTwo
    PageTwo.main()
elif st.session_state.page == 'page_three':
    import PageThree
    PageThree.main()


if menü == "Job Matcher": 
    import PageOne
    PageOne.main() 
if menü == "Klassische Job-Suche":
    import PageTwo
    PageTwo.main()
elif menü == "Gehaltsfinder":
    import PageThree
    PageThree.main()
