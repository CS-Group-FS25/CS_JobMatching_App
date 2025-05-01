import pandas as pd
import re
import os
from collections import Counter
import ast
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

skills_df = pd.read_csv("job_skills.csv", usecols=["job_link", "job_skills"])
jobs_df = pd.read_csv("linkedin_job_postings.csv", usecols=["job_link", "job_title", "search_position"])


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

def skills_to_clusters(skill_list):     # Matches a cluster to every skill in the skill list of each job
    return list({cluster_map[s] for s in skill_list if s in cluster_map})

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
        "service", "planner", "stylist", "staff", "surgeon", "management", "controller", "hospitalist",
        "estimator", "tutor", "buyer", "private", "mechanic", "holder", "practitioner", "banker", "conductor",
        "housekeeper", "driver", "recruiter", "oncology", "partner", "chemist", "server", "lecturer",
        "physiologist", "landscaper", "receptionist", "head", "maker", "videographer", "professor", "mentor",
        "auditor", "examiner", "principal", "anesthesiologist"
    ]

### CREATE DATAFRAME

v1_in_place = False
if not os.path.exists("matched_jobs_skills.csv"):       # check if df is already in place; if not, create df
    print("Create new data frame with jobs and skills by merging both data sets")

    ### clear list of empty entries and duplicates
    skills_df = skills_df.dropna().drop_duplicates()
    jobs_df = jobs_df.dropna().drop_duplicates()

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

    # jobs_df[jobs_df["matched"]].to_csv("jobtitles_cleaned_matched.csv", index=False)
    # jobs_df[~jobs_df["matched"]].to_csv("jobtitles_cleaned_unmatched.csv", index=False)

    ### merge jobs list and skills list by matching job link
    jobs_df = jobs_df.drop_duplicates(subset=["job_link"])      # Make sure no job link is double
    skills_df = skills_df.drop_duplicates(subset=["job_link"])

    matched_jobs_skills_df = pd.merge(jobs_df[jobs_df["matched"]], skills_df, on='job_link', how='inner')
    matched_jobs_skills_df.to_csv("matched_jobs_skills.csv", index=False)

else:   # if df in place, read the file
    print("Data Frame with jobs and matched skills is already in place")
    matched_jobs_skills_df = pd.read_csv("matched_jobs_skills.csv")
    v1_in_place = True

print("final shape of matched jobs and skills dataframe (should be 1180925, 7):", matched_jobs_skills_df.shape)

### SKILL CLUSTERING

n_skill_clusters = 150 # Defines into how many clusters the skills are divided
v2_in_place = False
if not os.path.exists("matched_jobs_skills_with_skill_cluster.csv") or v1_in_place == False:
    print("Clustering Skills...")
    if isinstance(matched_jobs_skills_df['job_skills_cleaned'].iloc[0], str):
        matched_jobs_skills_df['job_skills_cleaned'] = matched_jobs_skills_df['job_skills_cleaned'].apply(ast.literal_eval)
    matched_jobs_skills_with_skill_cluster_df = matched_jobs_skills_df
    all_skills = [skill for skill_list in matched_jobs_skills_with_skill_cluster_df['job_skills_cleaned'] for skill in skill_list]     # iterates through evey skill list in each line
    skill_counts = Counter(all_skills)
    print(len(skill_counts))
    skills_for_clustering = [skill for skill, count in skill_counts.items() if count >= 2][:50000]
    print(len(skills_for_clustering))

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(skills_for_clustering, show_progress_bar=True)

    kmeans = KMeans(n_clusters=n_skill_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(embeddings)

    df_clustered = pd.DataFrame({
        "skill": skills_for_clustering,
        "cluster": cluster_labels
    })

    df_clustered.sort_values(by="cluster").to_csv("clustered_skills.csv", index=False) # Create csv file with all 50'000 skills matched to one of 150 clusters

    cluster_map = dict(zip(df_clustered["skill"], df_clustered["cluster"]))
    matched_jobs_skills_with_skill_cluster_df["skill_clusters"] = matched_jobs_skills_with_skill_cluster_df["job_skills_cleaned"].apply(skills_to_clusters)
    matched_jobs_skills_with_skill_cluster_df.to_csv("matched_jobs_skills_with_skill_cluster.csv", index=False)
    print("Skills clustered in ", n_skill_clusters, " clusters!")
else:
    print("Skills already in ", n_skill_clusters, " clusters.")
    matched_jobs_skills_with_skill_cluster_df = pd.read_csv("matched_jobs_skills_with_skill_cluster.csv")
    v2_in_place = True

print("Final shape of matched jobs and skills with cluster dataframe (should be: 1180925, 8):", matched_jobs_skills_with_skill_cluster_df.shape)

### ONE-HOT ENCODING FOR SKILL CLUSTERS

v3_in_place = False
if not os.path.exists("skill_clusters_vectors.csv") or v2_in_place == False:
    print("Creating one dimensional vectors for each row...")
    mlb = MultiLabelBinarizer(classes=range(n_skill_clusters))    # Turns list of cluster numbers into a list with binary entries
    skill_cluster_matrix = mlb.fit_transform(matched_jobs_skills_with_skill_cluster_df["skill_clusters"])  # each line of df receives a one dimensional vector
    skill_clusters_vectors_df = pd.DataFrame(skill_cluster_matrix, columns=[f"cluster_{i}" for i in range(n_skill_clusters)])   # put clusters into different columns in df
    skill_clusters_vectors_df["job_title"] = matched_jobs_skills_with_skill_cluster_df["job_title_cleaned"]
    skill_clusters_vectors_df.to_csv("skill_clusters_vectors.csv", index=False)
    print("One dimensional vectors created!")
else:
    print("Skill cluster are already in one dimensional vector shape")
    skill_clusters_vectors_df = pd.read_csv("skill_clusters_vectors.csv")
    v3_in_place = True

print("Final shape of cluster vectors dataframe (should be 1180925, 151):", skill_clusters_vectors_df.shape)

### JOB TITLE CLUSTERING

v4_in_place = False
n_job_clusters = 500  # Defines into how many clusters the unique jobs are divided
if not os.path.exists("matched_jobs_skills_with_job_cluster.csv") or v3_in_place == False:
    print("Creating Job Clusters")
    unique_titles = matched_jobs_skills_df['job_title_cleaned'].dropna().unique().tolist()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    title_embeddings = model.encode(unique_titles, show_progress_bar=True)

    kmeans = KMeans(n_clusters=n_job_clusters, random_state=42)
    title_clusters = kmeans.fit_predict(title_embeddings)

    clustered_titles_df = pd.DataFrame({
        "original_title": unique_titles,
        "cluster_id": title_clusters
    })

    title_cluster_map = dict(zip(clustered_titles_df["original_title"], clustered_titles_df["cluster_id"]))
    matched_jobs_skills_with_job_cluster_df = matched_jobs_skills_df.copy()
    matched_jobs_skills_with_job_cluster_df["job_title_clustered"] = matched_jobs_skills_with_job_cluster_df["job_title_cleaned"].map(title_cluster_map)
    matched_jobs_skills_with_job_cluster_df.to_csv("matched_jobs_skills_with_job_cluster.csv", index=False)
else:
    print("Jobs are already clustered")
    matched_jobs_skills_with_job_cluster_df = pd.read_csv("matched_jobs_skills_with_job_cluster.csv")
    v4_in_place = True

### JOB INDUSTRY MATCHING

v5_in_place = False
if not os.path.exists("cluster_industry_preview.csv"):
    print("Creating file to manually match industries to job clusters")
    preview_jobs_per_cluster = (
        matched_jobs_skills_with_job_cluster_df
        .groupby("job_title_clustered")["job_title_cleaned"]    # to group job titles by clusters
        .apply(lambda titles: titles.value_counts().head(5).index.tolist())    # take out top 5 job titles of each cluster
        .reset_index()
        .rename(columns={"job_title_clustered": "cluster_id", "job_title_cleaned": "example_titles"})
    )

    preview_jobs_per_cluster["industry"] = ""
    preview_jobs_per_cluster.to_csv("cluster_industry_preview.csv", index=False)
    print("File created - Match the industries to the job clusters manually and then rerun the script")
    exit()
elif not v4_in_place:
    confirm = input("!! The following step resets your current industry allocation. Are you sure you want to proceed"
                    "and manually match the industries again? (yes/no)")
    if confirm.lower() != "yes":
        print("Process cancelled. Proceeding with current industry and potentially outdated job clusters")
    else:
        print("Creating file to manually match industries to job clusters")
        preview_jobs_per_cluster = (
            matched_jobs_skills_with_job_cluster_df
            .groupby("job_title_clustered")["job_title_cleaned"]  # to group job titles by clusters
            .apply(lambda titles: titles.value_counts().head(
                5).index.tolist())  # take out top 5 job titles of each cluster
            .reset_index()
            .rename(columns={"job_title_clustered": "cluster_id", "job_title_cleaned": "example_titles"})
        )

        preview_jobs_per_cluster["industry"] = ""
        preview_jobs_per_cluster.to_csv("cluster_industry_preview.csv", index=False)
        print("File created - Match the industries to the job clusters manually and then rerun the script")
        exit()
else:
    print("Industries are matched to job clusters and up to date!")
    job_clusters_with_industries_df = pd.read_csv("cluster_industry_preview.csv", encoding="cp1252")

### MACHINE LEARNING LOGIC

v6_in_place = False
if not os.path.exists("trained_random_forest.pkl") or v4_in_place == False:
    print("Training Model using Random Forest...")
    max_depth = 12     # depth of decision trees
    n_estimators = 75  # amount of decision trees

    filtered_df = matched_jobs_skills_with_job_cluster_df.dropna(subset=["job_title_clustered"]).copy()
    filtered_vectors_df = skill_clusters_vectors_df.loc[filtered_df.index].reset_index(drop=True)
    filtered_df = filtered_df.reset_index(drop=True)

    x = filtered_vectors_df.drop(columns=['job_title'])
    y = LabelEncoder().fit_transform(filtered_df['job_title_clustered'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    modelRFC = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        n_jobs=-1,
        verbose=1,
        random_state=42
    )
    modelRFC.fit(x_train, y_train)

    y_pred = modelRFC.predict(x_test)

    labels_in_test = set(y_test)
    labels_predicted = set(y_pred)
    relevant_labels = list(labels_in_test & labels_predicted)

    rfc_performance = classification_report(y_test, y_pred, labels=relevant_labels)
    with open("rfc_performance_report.txt", "w") as f:  # Save performance report of trained model in txt file
        f.write(rfc_performance)

    joblib.dump(modelRFC, "trained_random_forest.pkl") # Save trained model
    print("Training finished")
else:
    print("Model is already trained")
    modelRFC = joblib.load("trained_random_forest.pkl") # load saved model
    v6_in_place = True
