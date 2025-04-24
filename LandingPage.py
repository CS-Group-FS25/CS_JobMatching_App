import streamlit as st
import pandas as pd 
import numpy as np

st.set_page_config(page_title="Job Fit Application", page_icon=":briefcase:", layout="wide")

menü = st.sidebar.radio("Menu", ("Job Matcher", "Jobsuche nach Region", "Gehaltsfinder", "Über uns"))
st.title("Job Fit Application")
st.subheader("Wilkommen zu deinem personal Job Matcher")
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
if menü == "Job Matcher": 
    import PageOne
    PageOne.main() 
elif menü == "Gehaltsfinder":
    import PageThree
    PageThree.main()
