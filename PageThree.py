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
branchen = ["Buchhaltung & Finanzwesen","IT","Vertrieb","Kundendienst",
                "Ingenieur","HR", "Gesundheit", "Gastronomie","Marketing",
                "Logistik","Lehrer", "Bau", "Verwaltung","Rechtswesen",
                "Design", "Hochschulabsolventen", "Einzelhandel",
                "Consulting", "Fertigung", "Wissenschaft",
                "Sozialarbeit", "Tourismus","Energy", "Immobilien",
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


def datenabfrage(category): ### API-Abfrage zu Gehaltsdaten
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
        if "Minimum" in df.columns and pd.notnull(df["Minimum"].iloc[-1]):
            st.metric("Gehalt Minimum", f"{df['Minimum'].iloc[-1]:,.0f} €".replace(",", "."))
        else:
            st.metric("Gehalt Minimum", "k.A.")

        if "Maximum" in df.columns and pd.notnull(df["Maximum"].iloc[-1]):
            st.metric("Gehalt Maximum", f"{df['Maximum'].iloc[-1]:,.0f} €".replace(",", "."))
        else:
            st.metric("Gehalt Maximum", "k.A.")

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
        st.dataframe(df[["Monat", "Durchschnittsgehalt_fmt"]].rename(columns={"Durchschnittsgehalt_fmt": "Ø Gehalt"}), use_container_width=True)

def Gehaltssuche():
    st.title("Gehaltssuche nach Branche")
    st.subheader("Finde heraus, wie viel du in deiner Branche verdienen kannst!")
    auswahl = st.selectbox("Wähle eine Branche", branchen)
    category = branchen_mapping[auswahl]
    
    raw_data = datenabfrage(category)
    df = datenverarbeitung(raw_data)
    
    if df is not None:
        df["Durchschnittsgehalt_fmt"] = df["Durchschnittsgehalt"].apply(gehalt_formatierung)
        
        gehaltssuche_anzeigen(df)
        Gehaltsdiagramm(df, auswahl)
    else:
        st.warning("Keine Gehaltsdaten verfügbar. Bitte eine andere Branche auswählen.")
        

def main():
    Gehaltssuche()