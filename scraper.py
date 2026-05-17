import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


def get_jobs(job, location, experience):

    url = url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 10,
        "what": job,
       "where": location.split(",")[0]
    }

    try:

        response = requests.get(url, params=params)

        print(response.status_code)
        print(response.text)

        data = response.json()

        jobs = []

        for item in data.get("results", []):

            jobs.append({
                "title": item.get("title", "N/A"),
                "company": item.get("company", {}).get("display_name", "N/A"),
                "location": item.get("location", {}).get("display_name", "N/A"),
                "description": item.get("description", ""),
                "salary": item.get("salary_min", "Not Available"),
                "redirect_url": item.get("redirect_url", "#")
            })

        return jobs

    except Exception as e:
        print("ERROR:", e)
        return []