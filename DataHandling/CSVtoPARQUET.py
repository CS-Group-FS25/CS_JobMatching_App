import os.path
import pandas as pd

def csvtoparquet(url):
    encodings = ["utf-8", "ISO-8859-1", "cp1252"]
    if not os.path.exists(url + ".parquet"):
        for enc in encodings:
            try:
                df = pd.read_csv(url + ".csv", encoding=enc)
                df.to_parquet(url + ".parquet", index=False)
                print("CREATED NEW FILE!")
                break
            except Exception as e:
                print("Fehler mit Encoding", e)
    else:
        print("FILE ALREADY IN PLACE")

csvtoparquet("clustered_skills")
csvtoparquet("cluster_industry_preview")
csvtoparquet("job_skills")
csvtoparquet("linkedin_job_postings")
csvtoparquet("matched_jobs_skills")
csvtoparquet("matched_jobs_skills_with_job_cluster")
csvtoparquet("matched_jobs_skills_with_skill_cluster")
csvtoparquet("skill_clusters_vectors")