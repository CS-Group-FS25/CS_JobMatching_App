Das ist die Beschreibung der App von CS Gruppe Nr. 01.08 (Dominik Rück, Jakob Schäfer, Justus Rothdach, Nicolas Schmid). Das Ziel der App ist es, den perfekten Job basierend auf persönlichen Skills und Präferenzen zu finden.


INFO ÜBER INSTALLATION UND SETUP

Folgende Sachen müssen überprüft werden:
- Im Ordner DataHandling befinden sich die Dokumente mit exakt diesen file names:
      - cluster_industry_preview.parquet
      - clustered_skills.parquet
      - trained_random_forest_skills_only.pkl
  
- Im Ordner .streamlit befindet sich die config.toml Datei

- All Python Libraries aus requirements.txt wurden installiert

Achtung: Erstmaliger Start der App kann eventuell etwas länger brauchen, da die Dataframes und das ML Model geladen werden!


ALLGEMEINE INFO ZUR APP NUTZUNG

Die App hat 3 Hauptfunktionen: 
- Klassische Suche: Zeigt Job basierend auf Stichwort und Location an

- Persönlicher JobMatcher (Hauptfunktion): Input von persönlichem Profil inkl. Skills führt zum Vorschlag von 5 Jobs, die am besten zu einem passen. Dieser Prozess verwendet das trainierte ML Modell
  
- Job Dashboard (Hauptfunktion): Auf das Dashboard kann erst zugegriffen werden, wenn der Persönliche Matcher absolviert wurde. Das Dashboard zeigt die Top 5 Jobs des User an und ermöglicht einen Überblick über Gehalt und Jobangebote in der Nähe.
  
- Gehaltsfinder: Zeigt Durschnittsgehalt, Gehaltsverteilung und Gehaltstrend nach Branchen(wenn verfügbar) an


MÖLGICHE AUFTRETENDE BUGS UND LÖSUNGEN

- Auftreten einer leeren Fläche im Job Dashboard zwischen der Karte und der Jobangebote und Seite wird am unteren Ende geöffnet (Grund: laut Reddit ein Streamlit bug). Neuladen der Seite oder ein Wechsel zu einem anderen Job (über den Top 5 Jobs Tab) und wieder zurück zum bisherigen Job löst das Problem. 
- Verwendung der 3 grossen Menu Buttons auf der Startseite kann zu längerer Ladezeit führen (Grund: Verwendung von page_redirect). Sollte die Ladezeit zu lange sein, App neuladen und auf alternative Navigation über Sidebar Menu ausweichen. 


INFO ÜBER DATA HANDLING (IRRELEVANT FÜR APP SETUP & APP NUTZUNG)

Das Skript data_handling.py wurde dafür verwendet die Datensätze zu verarbeiten und ein Random Forest ML Model zu trainieren. Das Skript ist nicht notwendig für die Benutzung der App sondern dient lediglich der Erstellung wichtiger Dataframes ("cluster_industry_preview.parquet" & "clustered_skills.parquet"), sowie dem ML Model ("trained_random_forest_skills_only.pkl"). Nur diese 3 Dateien sind relevant für die Nutzung der App. Das Auführen von data_handling.py ist prinzipiell nicht notwendig, sofern keine Parameter im ML Model geändert oder die Anzahl der erstellten Job Cluster (default: 500) oder Skill Cluster (default: 150) geändert werden wollen.
Für das Ausführen von data_handling.py wird folgendes benötigt:
      - Download des Datensatzes von Kaggle: https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024/data
      - Zip Datei entpacken und die Dateien "job_skills.csv" und "linkedin_job_postings.csv" in den Ordner DataHandling ablegen
Nach dem Ausführen sollte noch einmal CSVtoPARQUET.py ausgeführt werden, damit alle Datensätze auch im .parquet Format vorliegen, da die App aus Geschwindigkeitsgründen mit diesem filytype arbeitet. 

