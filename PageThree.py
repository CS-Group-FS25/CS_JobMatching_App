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

### Branchen zur Auswahl definieren
branchen = ["Buchhaltung & Finanzwesen", "IT", "Vertrieb", "Kundendienst",
            "Ingenieur", "HR", "Gesundheit", "Gastronomie", "Marketing",
            "Logistik", "Lehrer", "Bau", "Verwaltung", "Rechtswesen",
            "Design", "Hochschulabsolventen", "Einzelhandel",
            "Consulting", "Fertigung", "Wissenschaft",
            "Sozialarbeit", "Tourismus", "Energy", "Immobilien",
            "Gemeinnützige Arbeit", "Reinigung", "Instandhaltung",
            "Teizeitstellen", "Sonstige"
            ]

# Mapping zu Adzuna-Categories
branchen_mapping = {
    "Buchhaltung & Finanzwesen": "accounting-finance-jobs",
    "IT": "it-jobs",
    "Vertrieb": "sales-jobs",
    "Kundendienst": "customer-services-jobs",
    "Ingenieur": "engineering-jobs",
    "HR": "hr-jobs",
    "Gesundheit": "healthcare-nursing-jobs",
    "Gastronomie": "hospitality-catering-jobs",
    "Marketing": "pr-advertising-marketing-jobs",
    "Logistik": "logistics-warehouse-jobs",
    "Lehrer": "teaching-jobs",
    "Bau": "trade-construction-jobs",
    "Verwaltung": "admin-jobs",
    "Rechtswesen": "legal-jobs",
    "Design": "creative-design-jobs",
    "Hochschulabsolventen": "graduate-jobs",
    "Einzelhandel": "retail-jobs",
    "Consulting": "consultancy-jobs",
    "Fertigung": "manufacturing-jobs",
    "Wissenschaft": "scientific-qa-jobs",
    "Sozialarbeit": "social-work-jobs",
    "Tourismus": "travel-jobs",
    "Versorgung": "energy-oil-gas-jobs",
    "Immobilien": "property-jobs",
    "Gemeinnützige Arbeit": "charity-voluntary-jobs",
    "Reinigung": "domestic-help-cleaning-jobs",
    "Instandhaltung": "maintenance-jobs",
    "Teizeitstellen": "part-time-jobs",
    "Sonstige": "other-jobs"
}


### Funktionen zur Spalte 1 - Gehaltsdaten
def datenabfrage(category):  ### API-Abfrage zu Gehaltsdaten
    ### API-Request
    url = f"https://api.adzuna.com/v1/api/jobs/ch/history?app_id={APP_ID}&app_key={APP_KEY}&category={category}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.write(f"Fehler in der Datenverarbeitung:{response.status_code}")
        return None


def datenverarbeitung(raw_data):
    if not raw_data or "month" not in raw_data:
        return None
    salary_data = raw_data["month"]

    if isinstance(list(salary_data.values())[0], dict):
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

    df["Monat"] = pd.to_datetime(df["Monat"], format='%Y-%m')
    df = df.sort_values("Monat")
    return df


def gehalt_formatierung(value):
    return f"{value:,.0f} €".replace(",", ".") if pd.notnull(value) else "k.A."


def gehaltssuche_anzeigen(df):
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📅 Letzter Monat", df["Monat"].max().strftime("%B %Y"))
        st.metric("💰 Gehalt zuletzt", f"{df['Durchschnittsgehalt'].iloc[-1]:,.0f} €".replace(",", "."))
    with col2:
        st.metric("Durchschnittsgehalt", f"{statistics.mean(df['Durchschnittsgehalt']):,.0f} €".replace(",", "."))


def Gehaltsdiagramm(df, auswahl):
    fig = px.line(
        df,
        x="Monat",
        y="Durchschnittsgehalt",
        title=f"Gehaltstrend für {auswahl}",
        labels={"Durchschnittsgehalt": "€"},
        markers=True
    )
    fig.update_layout(yaxis_tickformat=",.0f", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Optionale Tabelle
    with st.expander("📋 Rohdaten anzeigen"):
        st.dataframe(df[["Monat", "Durchschnittsgehalt_fmt"]].rename(columns={"Durchschnittsgehalt_fmt": "Ø Gehalt"}),
                     use_container_width=True)


### Funktionen zur Spalte 2 - Gehaltsverteilung
def datenabfrage_verteilung(category):  ### API-Abfrage zu Gehaltsverteilung
    url = f"http://api.adzuna.com/v1/api/jobs/ch/histogram?app_id={APP_ID}&app_key={APP_KEY}&category={category}&content-type=application/json"

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data.get("histogram", {})
    else:
        st.warning("Histogramm-Daten konnten nicht geladen werden.")
        return {}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def zeige_gehaltshistogramm(histogram_data):
    if not histogram_data:
        st.info("Keine Histogramm-Daten verfügbar.")
        return

    try:
        df_hist = pd.DataFrame([
            {"Gehalt": float(gehalt), "Anzahl": anzahl}
            for gehalt, anzahl in histogram_data.items()
            if is_number(gehalt)
        ])

    except ValueError as e:
        st.warning(f"Fehler bei der Umwandlung der Daten: {e}")
        return

    df_hist = df_hist.sort_values("Gehalt")

    max_gehalt = df_hist["Gehalt"].max()
    x_tick_step = 10000

    fig = px.bar(
        df_hist.sort_values("Gehalt"),
        x="Gehalt",
        y="Anzahl",
        title="Gehaltsverteilung (Histogramm)",
        labels={"Anzahl": "Jobanzahl", "Gehalt": "Gehalt (€)"}
    )
    fig.update_layout(
        xaxis=dict(
            range=[0, max_gehalt + x_tick_step],
            tickformat=",.0f",
            tickangle=45
        )
    )
    st.plotly_chart(fig, use_container_width=True)


### Abruf der Hauptfunktion
def main():
    st.title("Gehaltssuche nach Branche")
    st.subheader("Finde heraus, wie viel du in deiner Branche verdienen kannst!")
    auswahl = st.selectbox("Wähle eine Branche", branchen)
    category = branchen_mapping[auswahl]

    column1, column2 = st.columns(2)
    with column1:
        raw_data = datenabfrage(category)
        df = datenverarbeitung(raw_data)

        if df is not None:
            df["Durchschnittsgehalt_fmt"] = df["Durchschnittsgehalt"].apply(gehalt_formatierung)

            gehaltssuche_anzeigen(df)
            Gehaltsdiagramm(df, auswahl)
        else:
            st.warning("Keine Gehaltsdaten verfügbar. Bitte eine andere Branche auswählen.")

    with column2:
        histogram_data = datenabfrage_verteilung(category)

        if histogram_data:
            zeige_gehaltshistogramm(histogram_data)
        else:
            st.warning("Keine Gehaltsverteilung verfügbar. Bitte eine andere Branche auswählen.")