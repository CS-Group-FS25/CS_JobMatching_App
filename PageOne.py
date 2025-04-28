import streamlit as st

def page_one():
    st.write("PAGE ONE")

    #HIer soll die Jobmatching App sein

def api_google_jobs():
    api_key = ""

    import warnings
    warnings.filterwarnings("ignore", category=UserWarning) #Die API Abfrage gibt ansonsten eine Warnung ab, da 
#das urllib3-Modul, welches von requests verwendet wird (und damit auch von SerpApi), stattdessen OpenSSL ≥ 1.1.1 empfiehlt

    from serpapi import GoogleSearch

#Parameter für die anschliessende Suche

    location = st.text_input("Arbeitsort")
    hl = st.text_input("Sprache")
    gl = st.text_input("Land")

#folgende müssen zusammengefügt werden in den Parameter "q"
    job_beschreibung = st.text_input("Jobbeschreibung")
    soft_skills = st.text_input("Soft-Skills")


    params = {
     "engine": "google_jobs",
        "q": "Softwareentwickler", # "query"Hier könnte man allenfalls nach soft-skills suchen aber nur schlecht
        "location" : location, # Stadtname genügt meistens, funktioniert für nahezu alle Städte
        "hl": hl, #Sprache
        "gl": gl, #Land
     "api_key": api_key
}




    search = GoogleSearch(params)
    results = search.get_dict()

    for job in results.get("jobs_results", []):
        print(f"{job['title']} bei {job['company_name']} in {job['location']}")

