import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter
import ast
import joblib

def main():
    st.title("ML TEST")

    clustered_skills_df = pd.read_parquet("DataHandling/clustered_skills.parquet")

    skill_categories = {
        "Soft Skills & Kommunikation": [
            "communication", "verbal communication", "written communication",
            "teamwork", "collaboration", "interpersonal skills", "conflict resolution",
            "flexibility", "adaptability", "integrity", "reliability", "empathy",
            "professionalism", "motivation", "cultural sensitivity"
        ],
        "Problemlösung & Analyse": [
            "problem solving", "analytical skills", "critical thinking", "data analysis",
            "root cause analysis", "troubleshooting", "strategic thinking",
            "decision making", "machine learning", "research"
        ],
        "Führung & Management": [
            "leadership", "team leadership", "team management", "supervision",
            "project management", "operations management", "coaching",
            "mentoring", "stakeholder management", "change management"
        ],
        "Digitale & IT-Skills": [
            "microsoft office", "microsoft excel", "microsoft word",
            "computer skills", "software development", "sql", "python", "jira",
            "crm", "data analytics", "git", "cloud computing", "saas", "tableau"
        ],
        "Finanzen & Rechnungswesen": [
            "accounting", "budgeting", "financial analysis", "payroll",
            "tax preparation", "profitability", "financial planning", "cost control", "auditing"
        ],
        "Pflege, Gesundheit & Soziales": [
            "nursing", "patient care", "bls", "cpr", "medication administration",
            "emr", "acls", "rn license", "infection control", "social work", "therapy", "counseling"
        ],
        "Verkauf & Kundenkontakt": [
            "sales", "customer service", "retail", "merchandising", "upselling",
            "guest service", "store management", "cashier", "retail operations", "product knowledge"
        ],
        "Technik, Bau & Produktion": [
            "engineering", "construction management", "manufacturing",
            "mechanical engineering", "autocad", "sap", "process improvement",
            "welding", "hvac", "calibration"
        ],
        "Logistik & Organisation": [
            "inventory management", "logistics", "planning", "scheduling",
            "warehouse operations", "transportation", "shipping", "procurement",
            "supply chain management"
        ],
        "Administration & Organisation": [
            "documentation", "compliance", "reporting", "organization",
            "time management", "data entry", "record keeping", "policy development",
            "administrative support"
        ]
    }

    st.write("Wähle deine Skills aus:")

    cols = st.columns(5)
    category_names = list(skill_categories.keys())

    selected_skills = []

    for i in range(5):
        with cols[i]:
            for j in range(2):
                idx = i * 2 + j
                if idx < len(category_names):
                    cat = category_names[idx]
                    selected = st.multiselect(f"{cat}", skill_categories[cat], key=cat)
                    selected_skills.extend(selected)

    if selected_skills:
        st.write("🧠 **Ausgewählte Skills:**", selected_skills)

    matched_clusters = clustered_skills_df[clustered_skills_df["skill"].isin(selected_skills)]["cluster"].unique().tolist()

    st.write("Cluster IDs deiner Skills:", matched_clusters)

    model = joblib.load("DataHandling/trained_random_forest.pkl")

    all_clusters = sorted(clustered_skills_df["cluster"].unique())
    feature_vector = [1 if cluster in matched_clusters else 0 for cluster in all_clusters]

    industry_df = pd.read_parquet("DataHandling/cluster_industry_preview.parquet")
    industries = sorted(industry_df["industry"].dropna().unique())
    selected_industry = st.selectbox("Wähle eine Branche:", industries)

    industry_onehot = [1 if selected_industry == ind else 0 for ind in industries]

    x_input = np.array(feature_vector + industry_onehot).reshape(1, -1)

    predicted_job = model.predict(x_input)[0]

    st.success(f"🔮 Basierend auf deinen Skills und der Branche ist dein optimaler Job: **{predicted_job}**")