import streamlit as st
import numpy as np

def schaetze_gehalt(beruf, ort):
    # Simuliertes Gehaltsmodell (nur Beispiel!)
    basis_gehalt = {
        "Softwareentwickler": 60000,
        "Lehrer": 50000,
        "Koch": 32000,
        "Verkäufer": 30000,
        "Ingenieur": 58000,
    }

    ort_faktor = {
        "Berlin": 1.0,
        "München": 1.2,
        "Hamburg": 1.1,
        "Köln": 1.05,
        "Leipzig": 0.95,
    }

    beruf = beruf.title()
    ort = ort.title()

    grund = basis_gehalt.get(beruf, np.random.randint(30000, 60000))
    faktor = ort_faktor.get(ort, 1.0)
    return int(grund * faktor)

def main():
    st.title("💰 Gehaltsfinder")
    st.write("Erhalte eine Schätzung des durchschnittlichen Jahresgehalts basierend auf Beruf und Ort.")

    beruf = st.text_input("Beruf", "Softwareentwickler")
    ort = st.text_input("Ort", "Berlin")

    if st.button("💸 Gehalt schätzen"):
        st.spinner("Berechne Gehalt...")
        gehalt = schaetze_gehalt(beruf, ort)
        st.success(f"Das geschätzte Jahresgehalt in {ort} für einen {beruf} beträgt ca. **{gehalt:,} €**")
