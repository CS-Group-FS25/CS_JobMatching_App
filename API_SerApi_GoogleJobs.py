#API von SerpAPI
#WICHTIG zum testen: SerpAPI bietet einen "Playground" an bei welchem man 
#die verschiedenen variablen testen kann.
#so verschwenden wir keine Abfragen über den API Key selbst
#Damit der Code funktioniert muss pip install google-search-results installiert werden, ist umständlich
#Die API findet viele Jobs nahezu überall, allerdings sind soft-skills sehr schwer abzufragen

api_key = "4dd818979d563425bdc82e98c6de61b66d9940243f7ea7646352cb89ec2d78d2"

import warnings
warnings.filterwarnings("ignore", category=UserWarning) #Die API Abfrage gibt ansonsten eine Warnung ab, da 
#das urllib3-Modul, welches von requests verwendet wird (und damit auch von SerpApi), stattdessen OpenSSL ≥ 1.1.1 empfiehlt

from serpapi import GoogleSearch

params = {
    "engine": "google_jobs",
    "q": "Softwareentwickler", # "query"Hier könnte man allenfalls nach soft-skills suchen aber nur schlecht
    "location" : "St.Gallen", # Stadtname genügt meistens, funktioniert für nahezu alle Städte
    "hl": "de", #Sprache
    "gl": "ch", #Land
    "api_key": api_key
}

search = GoogleSearch(params)
results = search.get_dict()

for job in results.get("jobs_results", []):
    print(f"{job['title']} bei {job['company_name']} in {job['location']}") #es lassen sich 
    #viele weitere Angaben darstellen bei den Resultaten -> siehe Dokumentation

#Das ist mal eine einfache Abfrage für Softwareentwickler in St.Gallen
