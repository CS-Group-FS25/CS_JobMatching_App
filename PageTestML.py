import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter
import ast
import joblib

def styled_multiselect(label, options, key):
    st.markdown(f"<div style='min-height: 3em'><strong>{label}</strong></div>", unsafe_allow_html=True)
    return st.multiselect("", options, key=key)

def calculate_detailed_category_match(user_clusters_by_cat, job_cluster_id, matched_df, representative_df, cluster_to_meta):
    job_cluster_rows = matched_df[matched_df["job_title_clustered"] == job_cluster_id]
    job_cluster_lists = job_cluster_rows["skill_clusters"].apply(ast.literal_eval).tolist()
    all_clusters_flat = [cluster for sublist in job_cluster_lists for cluster in sublist]
    cluster_counts = Counter(all_clusters_flat)
    job_clusters = list(set(all_clusters_flat))
    cluster_top_skill_map = representative_df.drop_duplicates(subset=["cluster"]).set_index("cluster")["skill"].to_dict()
    job_representative_skills = [cluster_top_skill_map[c] for c in job_clusters if c in cluster_top_skill_map]
    st.write("Diese Skills sind typisch für das empfohlene Jobcluster:", job_representative_skills)
    job_cat_clusters = {}
    for c in job_clusters:
        cat = cluster_to_meta.get(c)
        if cat:
            job_cat_clusters.setdefault(cat, []).append(c)
    st.write("Für den Job benötigt:", job_cat_clusters)
    results = {}
    all_categories = list(set(cluster_to_meta.values()))
    for cat in all_categories:
        user_clusters = set(user_clusters_by_cat.get(cat, []))
        job_clusters_in_cat = set(job_cat_clusters.get(cat, []))
        if not job_clusters_in_cat:
            match_score = 100.0
            missing_skills = []
        elif not user_clusters:
            match_score = 0.0
            missing_skills = [cluster_top_skill_map.get(c) for c in job_clusters_in_cat]
        else:
            overlap = user_clusters & job_clusters_in_cat
            match_score = round(len(overlap) / len(job_clusters_in_cat) * 100, 1)
            missing_clusters = job_clusters_in_cat - user_clusters
            missing_skills = [cluster_top_skill_map.get(c) for c in missing_clusters]
        results[cat] = {
            "matching_percent": match_score,
            "missing_skills": [s for s in missing_skills if s]
        }
    return results

def build_user_clusters_by_category(skill_categories, selected_skills_by_cat, clustered_skills_df):
    skill_to_cluster = dict(zip(clustered_skills_df["skill"], clustered_skills_df["cluster"]))
    user_clusters_by_cat = {}
    for cat, skills in selected_skills_by_cat.items():
        clusters = [skill_to_cluster.get(skill) for skill in skills if skill_to_cluster.get(skill) is not None]
        if clusters:
            user_clusters_by_cat[cat] = list(set(clusters))
    return user_clusters_by_cat

def create_cluster_to_meta_mapping(skill_categories, clustered_skills_df):
    skill_to_category = {}
    for category, skills in skill_categories.items():
        for skill in skills:
            skill_to_category[skill] = category
    skill_to_cluster = dict(zip(clustered_skills_df["skill"], clustered_skills_df["cluster"]))
    cluster_to_meta = {}
    for skill, cluster in skill_to_cluster.items():
        if skill in skill_to_category:
            cluster_to_meta[cluster] = skill_to_category[skill]
    return cluster_to_meta

def get_skill_clusters_for_jobs(example_titles, skill_vector_df, representative_df):
    job_title_col = skill_vector_df.columns[-1]
    cluster_cols = skill_vector_df.columns[:-1]
    job_to_clusters = {}
    cluster_top_skill_map = representative_df.drop_duplicates(subset=["cluster"]).set_index("cluster")["skill"].to_dict()
    for title in example_titles:
        matches = skill_vector_df[skill_vector_df[job_title_col].str.lower() == title.lower()]
        if not matches.empty:
            row = matches.iloc[0]
            active_clusters = [int(col.replace("cluster_", "")) for col in cluster_cols if row[col] == 1]
            top_skills = [cluster_top_skill_map.get(c) for c in active_clusters if c in cluster_top_skill_map]
            job_to_clusters[title] = {
                "clusters": active_clusters,
                "skills": top_skills
            }
        else:
            job_to_clusters[title] = {
                "clusters": [],
                "skills": []
            }
    return job_to_clusters

def main():
    st.title("ML TEST")

    clustered_skills_df = pd.read_parquet("DataHandling/clustered_skills.parquet")
    clustered_jobs_with_industry = pd.read_parquet("DataHandling/cluster_industry_preview.parquet")
    matched_df = pd.read_parquet("DataHandling/matched_jobs_skills_with_job_cluster.parquet")
    representative_df = pd.read_csv("DataHandling/representative_skills_per_cluster.csv")
    industry_df = pd.read_parquet("DataHandling/cluster_industry_preview.parquet")
    skill_vector_df = pd.read_csv("DataHandling/skill_clusters_vectors.csv")

    skill_categories = {
        "Analytik & Problemlösung": [
            "data modeling", "problemsolving skills", "mathematical calculations", "testing", "critical thinking",
            "assessment", "data analysis", "analytical thinking", "machine learning", "problem solving",
            "strategic thinking", "inspections", "attention to detail", "quality control",
            "standard operating procedures"
        ],
        "Digitale & Technische Kompetenzen": [
            "javascript", "python", "sql", "systems engineering", "computer literacy", "cloud computing",
            "technical knowledge", "sap", "autocad", "revit", "design", "electrical engineering",
            "mechanical engineering",
            "manufacturing", "pipeline management"
        ],
        "Kommunikation & Zusammenarbeit": [
            "teamwork", "active listening", "communication skills", "empathy", "collaboration", "mentoring",
            "supervision", "public relations", "presentation skills", "cultural sensitivity", "leadership skills",
            "client relationship management", "recruitment", "negotiation", "employee communication"
        ],
        "Management & Organisation": [
            "performance management", "strategic planning", "inventory management", "process optimization",
            "organization", "policy development", "project management", "operations management",
            "business development", "logistics", "budgeting", "financial analysis", "auditing", "event coordination",
            "time management"
        ],
        "Ausbildung & Qualifikationen": [
            "bachelor’s degree", "bachelor’s degree in nursing", "bls certification", "acls", "cme allowance",
            "nursing", "healthcare", "emr", "teaching", "credentialing", "certifications", "chemistry", "microbiology",
            "legal research", "cosmetology license"
        ],
        "Medizinisch / Pflege & Therapie": [
            "surgical procedures", "physiology", "medical terminology", "treatment planning", "care planning",
            "stress management", "crisis intervention", "patient care", "ventilator management", "medical benefits",
            "nursing license", "medical imaging", "radiography", "healthcare", "emr"
        ],
        "Handwerk & Physische Tätigkeiten": [
            "cleanliness", "maintenance", "heavy lifting", "physical strength", "hvac", "environmental engineering",
            "construction management", "inspections", "hospitality", "food service", "cleaning",
            "physical requirements",
            "driving license", "house maintenance", "safety standards"
        ],
        "Verkauf, Kundenservice & Einzelhandel": [
            "sales management", "customer service skills", "guest service", "retail management", "retail experience",
            "cash handling", "cash register operation", "store management", "upselling", "merchandising",
            "client communication", "product knowledge", "hospitality", "public service", "employee discounts"
        ],
        "Verwaltung, Finanzen & Buchhaltung": [
            "financial reporting", "invoicing", "accounting", "tax preparation", "401k retirement plan",
            "loan processing", "compliance", "reporting", "sql", "documentation", "medical records", "credentialing",
            "ts/sci clearance", "employee assistance program", "pto"
        ],
        "Arbeitgeberleistungen & Erwartungen": [
            "paid holidays", "competitive salary", "remote work", "employee assistance program", "clean driving record",
            "flexible hours", "free parking", "tuition reimbursement", "paid time off", "physical requirements",
            "basic life support (bls)", "high school diploma", "5+ years of experience", "fastpaced environment",
            "flexible work schedule"
        ]
    }

    cluster_to_meta = create_cluster_to_meta_mapping(skill_categories, clustered_skills_df)

    ## BIS HIER VIELLEICHT ALLES IN EINE INIT?

    st.write("Wähle deine Skills aus:")

    cols = st.columns(5)
    category_names = list(skill_categories.keys())

    selected_skills_by_cat = {}

    # Zeile 1
    cols_row1 = st.columns(5)
    for i in range(5):
        cat = category_names[i]
        with cols_row1[i]:
            selected = styled_multiselect(cat, skill_categories[cat], key=cat)
            if selected:
                selected_skills_by_cat[cat] = selected

    # Zeile 2
    cols_row2 = st.columns(5)
    for i in range(5, 10):
        cat = category_names[i]
        with cols_row2[i - 5]:
            selected = styled_multiselect(cat, skill_categories[cat], key=cat)
            if selected:
                selected_skills_by_cat[cat] = selected

    industries = sorted(industry_df["industry"].dropna().unique())
    selected_industry = st.selectbox("Wähle eine Branche:", industries)

    if st.button("🔍 Suche passenden Job"):
        selected_skills = [skill for skills in selected_skills_by_cat.values() for skill in skills] # Speichere das Dictionary selected_skills_by_cat in eine flache Liste

        if not selected_skills:
            st.warning("Bitte wähle mindestens einen Skill aus.")
        else:
            st.write("**Ausgewählte Skills:**", selected_skills)

            matched_clusters = clustered_skills_df[clustered_skills_df["skill"].isin(selected_skills)][
                "cluster"].unique().tolist()
            st.write("Cluster IDs deiner Skills:", matched_clusters)

            model, industry_encoder = joblib.load("DataHandling/trained_random_forest_with_industry.pkl")

            all_clusters = sorted(clustered_skills_df["cluster"].unique())
            feature_vector = [1 if cluster in matched_clusters else 0 for cluster in all_clusters]

            industry_onehot = industry_encoder.transform([[selected_industry]])[0]

            x_input = np.array(feature_vector + list(industry_onehot)).reshape(1, -1)

            predicted_job_cluster = model.predict(x_input)[0]

            user_clusters_by_cat = build_user_clusters_by_category(
                skill_categories,
                selected_skills_by_cat,
                clustered_skills_df
            )

            st.write(user_clusters_by_cat)

            st.success(
                f"Basierend auf deinen Skills und der Branche ist dein optimaler Job: **{predicted_job_cluster}**")

            ### Predict Probability
            probas = model.predict_proba(x_input)[0]
            predicted_cluster_index = list(model.classes_).index(predicted_job_cluster)
            predicted_probability = round(probas[predicted_cluster_index] * 100, 2)

            st.info(
                f"Wahrscheinlichkeit für das empfohlene Jobcluster ({predicted_job_cluster}): **{predicted_probability}%**")

            '''### Skill Overlap mit Job (nicht für die App verwenden wahrscheinlich!)
            row = clustered_jobs_with_industry[clustered_jobs_with_industry["cluster_id"] == predicted_job_cluster]

            if not row.empty:
                title_str = row["example_titles"].values[0]
                example_titles = ast.literal_eval(title_str)

                st.write("**Top 5 Jobs für dich:**")
                for title in example_titles:
                    st.markdown(f"- {title}")

                # ✨ Neue Integration hier: Cluster IDs und Skills pro Job extrahieren
                job_to_clusters = get_skill_clusters_for_jobs(example_titles, skill_vector_df, representative_df)

                st.markdown("### 🧠 Skill-Cluster-Matching für deine Top 5 Jobs:")

                # 1. Alle vom User gewählten Cluster
                user_clusters = set()
                for cluster_list in user_clusters_by_cat.values():
                    user_clusters.update(cluster_list)

                for job, data in job_to_clusters.items():
                    job_clusters = set(data["clusters"])
                    if not job_clusters:
                        st.warning(f"🔸 {job}: Keine Skill-Cluster-Daten verfügbar.")
                        continue

                    overlap = user_clusters & job_clusters
                    match_score = round(len(overlap) / len(job_clusters) * 100, 1)
                    missing_clusters = job_clusters - user_clusters
                    missing_skills = [s for c, s in zip(data["clusters"], data["skills"]) if c in missing_clusters]

                    st.markdown(f"**{job}**")
                    st.markdown(f"✅ Übereinstimmung: **{match_score}%**")
                    if missing_skills:
                        st.markdown(f"❌ Fehlende Skills: {', '.join(missing_skills)}")
                    else:
                        st.markdown("🎉 Alle nötigen Skills vorhanden!")
            else:
                st.warning("Es konnten keine passenden Jobs für dich gefunden werden.")

            detailed_results = calculate_detailed_category_match(
                user_clusters_by_cat=user_clusters_by_cat,
                job_cluster_id=predicted_job_cluster,
                matched_df=matched_df,
                representative_df=representative_df,
                cluster_to_meta=cluster_to_meta
            )'''
