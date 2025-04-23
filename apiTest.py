from serpapi import GoogleSearch

params = {
    "engine": "google_jobs",
    "q": "Marketing Praktikum Zürich",
    "location": "Zürich, Schweiz",
    "api_key": "a0fa6e0e717278ab5d2a09a6b7d43a94842ab7807536cb7761246c14664cd689"
}

search = GoogleSearch(params)
results = search.get_dict()

# Ergebnisse durchgehen
for job in results.get("jobs_results", []):
    print(job["title"])
    print(job["company_name"])
    print(job["location"])
    print(job["via"])  # z.B. LinkedIn, Glassdoor etc.
    print(job["description"][:150], "...\n")  # kurze Vorschau
    print(job["description"][:150], "...\n")  # kurze Vorschau


print("Hello thats new!")