import pandas as pd
import re
from collections import Counter

skills_df = pd.read_csv("DataHandling/job_skills.csv", usecols=["job_link", "job_skills"])
jobs_df = pd.read_csv("DataHandling/linkedin_job_postings.csv", usecols=["job_link", "job_title", "search_position"])


uncleaned_title = [] # only for testing - delete later!

def extract_job_core(title):
    separators = r"[-–•|/,.\s]{2,}"
    title = str(title).lower()
    parts = re.split(separators, title)
    parts = [p.strip() for p in parts if p.strip()]

    for part in parts:
        for keyword in job_keywords:
            if keyword in part:
                return part.title()
    uncleaned_title.append(title)
    return title.title()    # Default return when no keyword is found

job_keywords = [
        "engineer", "developer", "manager", "designer", "consultant", "analyst",
        "specialist", "technician", "coordinator", "director", "officer",
        "scientist", "assistant", "architect", "administrator", "nurse", "teacher",
        "sales", "marketing", "intern", "writer", "accountant", "editor", "executive",
        "supervisor", "counselor", "model", "physician", "physicist", "psychologist", "trainer", "professional",
        "associate", "instructor", "producer", "therapist", "clerk", "chef", "surveyor", "advisor", "adviser",
        "host", "technologist", "researcher", "agent", "leader", "finance", "provider", "ambassador",
        "maintenance", "generalist", "representative", "tester", "superintendent", "lead", "senior", "volunteer",
        "inspector", "attorney", "cook", "general", "veterinarian", "dentist", "advocate", "cashier", "worker",
        "attendant", "medical", "coach", "guest", "operator", "psychiatrist", "foreman", "emergency", "clinical",
        "service", "planner", "stylist", "staff", "surgeon", "management", "controller", "pediatric", "hospitalist",
        "estimator", "tutor", "buyer", "private", "mechanic", "holder", "practitioner", "banker", "conductor",
        "housekeeper", "driver", "recruiter", "oncology", "partner", "chemist", "server", "lecturer",
        "physiologist", "landscaper", "receptionist", "head", "maker", "videographer", "professor", "mentor",
        "auditor", "examiner", "principal",
    ]

### clear list of empty entries and duplicates
skills_df.dropna()
skills_df.drop_duplicates()
jobs_df.dropna()
jobs_df.drop_duplicates()

### normalize skills list
skills_df['job_skills_cleaned'] = skills_df['job_skills'].apply(
    lambda x: [s.strip().lower() for s in str(x).split(',')] if pd.notnull(x) else []
)

### clean job title
jobs_df["job_title_cleaned"] = jobs_df["job_title"].apply(extract_job_core)
print(uncleaned_title)
print(len(uncleaned_title))

word_counter = Counter()

for title in uncleaned_title:
    words  = re.findall(r"\w+", title.lower())
    word_counter.update(words)

print(word_counter.most_common(50))

jobs_df["matched"] = jobs_df["job_title_cleaned"].str.lower().apply(
    lambda t: any(keyword in t for keyword in job_keywords)
)

# jobs_df[jobs_df["matched"]].to_csv("DataHandling/jobtitles_cleaned_matched.csv", index=False)
# jobs_df[~jobs_df["matched"]].to_csv("DataHandling/jobtitles_cleaned_unmatched.csv", index=False)

### merge both jobs and skills list by matching job link
matched_jobs_skills_df = pd.merge(jobs_df, skills_df, on='job_link', how='inner')
matched_jobs_skills_df.to_csv("DataHandling/matched_jobs_skills.csv", index=False)
print("final shape:", matched_jobs_skills_df.shape)






