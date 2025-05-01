import streamlit as st
import pandas as pd 
import numpy as np

st.set_page_config(page_title="Job Fit App", page_icon=":briefcase:", layout="wide")

if "seite" not in st.session_state:
    st.session_state.seite = "Startseite"
# Initialisierung von session_state.button, wir abgefragt ob ein button geclickt wurde
if "button" not in st.session_state: 
    st.session_state.button = False


st.write(f"Ausgewählt: {selected}")

menü = st.sidebar.radio("Menu", ("Startseite", "Job Matcher", "Jobsuche nach Region", "Gehaltsfinder", "Über uns"))
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

col1, col2, col3 = st.columns(3)
with col1:
    if st.button('JobMatcher'):
        import PageOne
        PageOne.main()
with col2:
    if st.button('Klassische Job-Suche'):
        import PageTwo
        PageTwo.main()
with col3:
    if st.button('Gehaltsfinder'):
        import PageThree
        PageThree.main()
    


if menü == "Job Matcher": 
    import PageOne
    PageOne.main() 
elif menü == "Gehaltsfinder":
    import PageThree
    PageThree.main()
