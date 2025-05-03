import streamlit as st
import pandas as pd 
import numpy as np
import requests

def main():
    st.set_page_config(page_title="Job Fit App", page_icon=":briefcase:", layout="wide")

    ### session_state
    if 'page' not in st.session_state:
        st.session_state.page = 'Startseite'

    menü = st.sidebar.radio("Menu", ("Startseite", "Job Matcher", "Klassische Job-Suche", "Gehaltsfinder", "Über uns"))

    if menü != "Startseite":
        st.session_state.page = menü

    if st.session_state.page == "Startseite":    
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
        col1, col2, col3 = st.columns([ 1, 1, 1 ])
        with col1:
            if st.button('JobMatcher'):
                st.session_state.page = "Job Matcher"
                import PageOne
                PageOne.main()
        with col2:
            if st.button('Klassische Job-Suche'):
                st.session_state.page = "Klassische Job-Suche"
                import PageTwo
                PageTwo.main()
        with col3:
            if st.button('Gehaltsfinder'):
                st.session_state.page = "Gehaltsfinder"
                import PageThree
                PageThree.main()
        
        
        
        
        
        
    elif st.session_state.page == "Job Matcher": 
        import PageOne
        PageOne.main() 
    elif st.session_state.page == "Klassische Job-Suche":
        import PageTwo
        PageTwo.main()
    elif st.session_state.page == "Gehaltsfinder":
        import PageThree
        PageThree.main()
    elif st.session_state.page == "Über Uns":
        import PageFour
        PageFour.main()

main()



   





