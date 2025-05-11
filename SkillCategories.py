import streamlit as st

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

# cluster_to_meta = create_cluster_to_meta_mapping(skill_categories, st.session_state.clustered_skills_df)