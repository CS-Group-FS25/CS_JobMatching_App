import streamlit as st
import numpy as np
import requests
import statistics


# Adzuna API Einrichten mit API ID und Schlüssel
APP_ID = "42d55acf"
APP_KEY = "2fde9c1ff58d9bfdf254dd3f0c4d6ec7"
url = f'https://api.adzuna.com/v1/api/jobs/ch/search/1'


def Gehaltssuche():
    st.title("Gehaltssuche nach Branche")
    ### Auswahl der Branche nach deren Gehalt man sucht (nur eine Branche wählbar)
    branche = st.selectbox("Wähle die Branche nach welcher du suchst?",
                           ("Finanzen","IT & Software", "Vertrieb", 
                            "Kundendienst", "Ingenieur", "HR","Pflege")                           
                           )
    Ort = st.text_input("In welcher Region suchst du?")
    
    if st.button("Gehalt anzeigen"):
        parameter = {
            'app_id' : APP_ID,
            'app_key': APP_KEY,
            'what' : branche, 
            'results per page' : 20,
            'salary_include_unknown' : 0
        }
        
        if Ort:
            parameter['where'] = Ort
        url = 'https://api.adzuna.com/v1/api/jobs/de/search/1'
        response = requests.get(url, params=parameter)
            
        if response.status_code == 200:
            jobs = response.json().get('results', [])
            gehaelter = [job['salary_avg'] for job in jobs if job.get('salary_avg')]

            if gehaelter:
                st.success(f"🔢 Gefundene Jobs mit Gehalt: {len(gehaelter)}")
                st.metric("Durchschnittsgehalt", f"{int(statistics.mean(gehaelter)):,} CHF")
                st.metric("Minimum", f"{int(min(gehaelter)):,} CHF")
                st.metric("Maximum", f"{int(max(gehaelter)):,} CHF")

                st.bar_chart(gehaelter)
            else:
                st.warning("Keine Gehaltsdaten gefunden.")
        else:
            st.error(f"Fehler bei der API-Anfrage: {response.status_code}")    


def main():
   Gehaltssuche()
   

