import streamlit as st
import numpy as np
import requests
import statistics
import pandas as pd
import plotly.express as px

# Adzuna API Einrichten mit API ID und Schlüssel
APP_ID = "42d55acf"
APP_KEY = "2fde9c1ff58d9bfdf254dd3f0c4d6ec7"
url = f'https://api.adzuna.com/v1/api/jobs/ch/search/1'

# Branchen zur Auswahl definieren
branchen = ["Buchhaltung & Finanzwesen", "IT", "Vertrieb", "Kundendienst",
            "Techniker", "Personal & Personalbeschaffung", "Gesundheitswesen & Pflege", 
            "Gastronomie & Catering", "PR, Werbung & Marketing",
            "Logistik & Lagerhaltung", "Lehrberufe", "Handel & Bau", 
            "Verwaltung", "Juristische Berufe",
            "Kreation & Design", "Hochschulabsolventen", "Einzelhandel",
            "Beratung", "Fertigung", "Wissenschaft & Qualitätssicherung",
            "Sozialarbeit", "Tourismus", "Versorgungsunternehmen", 
            "Immobilien", "Gemeinnützige & ehrenamtliche Arbeit", 
            "Haushaltshilfen & Reinigung", "Wartung", "Teilzeit", 
            "Sonstige/Allgemeine Stellen"
            ]

# Mapping zu Adzuna-Categories für die API-Abfrage
branchen_mapping = {
    "Buchhaltung & Finanzwesen": "accounting-finance-jobs",
    "IT": "it-jobs",
    "Vertrieb": "sales-jobs",
    "Kundendienst": "customer-services-jobs",
    "Techniker": "engineering-jobs",
    "Personal & Personalbeschaffung": "hr-jobs",
    "Gesundheitswesen & Pflege": "healthcare-nursing-jobs",
    "Gastronomie & Catering": "hospitality-catering-jobs",
    "PR, Werbung & Marketing": "pr-advertising-marketing-jobs",
    "Logistik & Lagerhaltung": "logistics-warehouse-jobs",
    "Lehrberufe": "teaching-jobs",
    "Handel & Bau": "trade-construction-jobs",
    "Verwaltung": "admin-jobs",
    "Juristische Berufe": "legal-jobs",
    "Kreation & Design": "creative-design-jobs",
    "Hochschulabsolventen": "graduate-jobs",
    "Einzelhandel": "retail-jobs",
    "Beratung": "consultancy-jobs",
    "Fertigung": "manufacturing-jobs",
    "Wissenschaft & Qualitätssicherung": "scientific-qa-jobs",
    "Sozialarbeit": "social-work-jobs",
    "Tourismus": "travel-jobs",
    "Versorgungsunternehmen": "energy-oil-gas-jobs",
    "Immobilien": "property-jobs",
    "Gemeinnützige & ehrenamtliche Tätigkeiten": "charity-voluntary-jobs",
    "Haushaltshilfen & Reinigung": "domestic-help-cleaning-jobs",
    "Wartung": "maintenance-jobs",
    "Teilzeit": "part-time-jobs",
    "Sonstige/Allgemeine Stellen": "other-general-jobs"
}

# Funktionen zur Spalte 1 - Gehaltsdaten
def datenabfrage(category):  # API-Abfrage zu Gehaltsdaten
    # API-Request
    url = f"https://api.adzuna.com/v1/api/jobs/ch/history?app_id={APP_ID}&app_key={APP_KEY}&category={category}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.write(f"Fehler in der Datenverarbeitung:{response.status_code}")
        return None

# Funktion zur Datenverarbeitung
def datenverarbeitung(branche):
    category = branchen_mapping[branche]
    # Speichern der API-Daten in einer Variablen
    raw_data = datenabfrage(category)

    if not raw_data or "month" not in raw_data:
        return pd.DataFrame(), category
    
    salary_data = raw_data["month"]
    
    if not salary_data:
        return pd.DataFrame(), category
    
    # Überprüfen, ob die Gehaltsdaten in einem Dictionary-Format vorliegen
    try: 
        if isinstance(list(salary_data.values())[0], dict):
            # Gehaltsdaten in DataFrame umwandeln
            df = pd.DataFrame([
                {
                    "Monat": month,
                    "Durchschnittsgehalt": werte.get("average"),
                    "Minimum": werte.get("min"),
                    "Maximum": werte.get("max")
                }
                for month, werte in salary_data.items()
            ])
        else:
            df = pd.DataFrame([
                {"Monat": month, "Durchschnittsgehalt": gehalt}
                for month, gehalt in salary_data.items()
            ])
    except Exception as e:
        st.warning(f"Fehler bei der Umwandlung der Gehaltsdaten: {e}")
        return pd.DataFrame(), category
    
    if df.empty or "Durchschnittsgehalt" not in df.columns:
        return pd.DataFrame(), category
    
    # Darstellung der Gehaltsdaten nach Monat sortiert
    df["Monat"] = pd.to_datetime(df["Monat"], format='%Y-%m', errors="coerce")
    df = df.sort_values("Monat")
    return df, category

# Funktion zur Formatierung des Gehalts
def gehalt_formatierung(value):
    return f"{value:,.0f} CHF".replace(",", ".") if pd.notnull(value) else "k.A."

# Funktion zur Anzeige der Gehaltsdaten
def gehaltssuche_anzeigen(df):
    # Zwei Spalten für die Anzeige der Gehaltsdaten
    col1, col2 = st.columns(2)
    with col1:
        # Anzeige der Gehaltsdaten( Letzter Moant, Gehalt zuletzt)
        st.metric("📅 Letzter Monat", df["Monat"].max().strftime("%B %Y"))
        st.metric("💰 Gehalt zuletzt", f"{df['Durchschnittsgehalt'].iloc[-1]:,.0f} CHF".replace(",", "."))
    with col2:
        # Anzeige des Durchschnittsgehalts
        st.metric("Durchschnittsgehalt", f"{statistics.mean(df['Durchschnittsgehalt']):,.0f} CHF".replace(",", "."))

# Funktion Gehaltsdiagramm (Liniendiagramm)
def gehaltsdiagramm(df, auswahl, show_raw=True, dashboard=False):
    if "Durchschnittsgehalt_fmt" not in st.session_state.df_salary.columns:
        st.session_state.df_salary["Durchschnittsgehalt_fmt"] = (st.session_state.df_salary
                                                                 ["Durchschnittsgehalt"]
                                                                 .apply(gehalt_formatierung))
    fig = px.line(
        df,
        x="Monat",
        y="Durchschnittsgehalt",
        title=f"Gehaltstrend für {auswahl}",
        labels={"Durchschnittsgehalt": "CHF"},
        markers=True
    )
    sec_bg = st.session_state.sec_bg_color
    fig.update_traces(line=dict(color=sec_bg))
    fig.update_layout(yaxis_tickformat=",.0f", hovermode="x unified")

    if dashboard:
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.plotly_chart(fig, use_container_width=True)

    # Optionale Tabelle
    if show_raw:
        with st.expander("📋 Rohdaten anzeigen"):
            st.dataframe(df[["Monat", "Durchschnittsgehalt_fmt"]].rename(columns={"Durchschnittsgehalt_fmt": "Ø Gehalt"}),
                         use_container_width=True)


# Funktionen zur Spalte 2 - Gehaltsverteilung
def datenabfrage_verteilung(category):  ### API-Abfrage zu Gehaltsverteilung
    url = f"http://api.adzuna.com/v1/api/jobs/ch/histogram?app_id={APP_ID}&app_key={APP_KEY}&category={category}&content-type=application/json"

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data.get("histogram", {})
    else:
        st.warning("Histogramm-Daten konnten nicht geladen werden.")
        return {}

# Basic Funktion zur Überprüfung, ob ein Wert eine Zahl ist
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Funktion zur Anzeige des Gehaltshistogramms
def zeige_gehaltshistogramm(histogram_data, dashboard=False):
    if not histogram_data:
        st.info("Keine Histogramm-Daten verfügbar.")
        return

    try:
        # Histogramm anzeigen und Umwandung von Gehalt in float
        df_hist = pd.DataFrame([
            {"Gehalt": float(gehalt), "Anzahl": anzahl}
            for gehalt, anzahl in histogram_data.items()
            if is_number(gehalt)
        ])

    except ValueError as e:
        st.warning(f"Fehler bei der Umwandlung der Daten: {e}")
        return
    #Sortierung 
    df_hist = df_hist.sort_values("Gehalt")
    # X-Achse Länge um  10000 erhöhen
    max_gehalt = df_hist["Gehalt"].max()
    x_tick_step = 10000
    
    # Balkendiagramm erstellen
    fig = px.bar(
        df_hist.sort_values("Gehalt"),
        x="Gehalt",
        y="Anzahl",
        title="Gehaltsverteilung (Histogramm)",
        labels={"Anzahl": "Jobanzahl", "Gehalt": "Gehalt (CHF)"}
    )
    # Farbanpassung 
    sec_bg = st.session_state.sec_bg_color
    fig.update_traces(marker=dict(color=sec_bg))
    
    # Darstellung der Gehaltsverteilung
    if dashboard:
        fig.update_layout(
            height=300,
            xaxis=dict(
                range=[0, max_gehalt + x_tick_step],
                tickformat=",.0f",
                tickangle=45
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        fig.update_layout(
            xaxis=dict(
                range=[0, max_gehalt + x_tick_step],
                tickformat=",.0f",
                tickangle=45
            )
        )
        st.plotly_chart(fig, use_container_width=True)

# Abruf der Hauptfunktion
def main():
    st.title("Gehaltssuche nach Branche")
    st.subheader("Finde heraus, wie viel du in deiner Branche verdienen kannst!")
    auswahl = st.selectbox("Wähle eine Branche", branchen)
    category = branchen_mapping[auswahl]
    
    if st.session_state.get("category") != category:
        st.session_state.category = category
        st.session_state.df_salary, _ = datenverarbeitung(auswahl)
        st.session_state.histogram_data = datenabfrage_verteilung(category)
    
    column1, column2 = st.columns(2)
    with (column1):
        if st.session_state.df_salary is not None and not st.session_state.df_salary.empty:
            if "Durchschnittsgehalt_fmt" not in st.session_state.df_salary.columns:
                st.session_state.df_salary["Durchschnittsgehalt_fmt"] = (
                    st.session_state.df_salary["Durchschnittsgehalt"]
                    .apply(gehalt_formatierung) 
                )
            gehaltssuche_anzeigen(st.session_state.df_salary)
            gehaltsdiagramm(st.session_state.df_salary, auswahl)
        else: 
            st.warning("Keine Gehaltsdaten verfügbar. Bitte eine andere Branche auswählen.")    
        
        
    with column2:
        if st.session_state.histogram_data:
            zeige_gehaltshistogramm(st.session_state.histogram_data)
        else:
            st.warning("Keine Gehaltsverteilung verfügbar. Bitte eine andere Branche auswählen.")