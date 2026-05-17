import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


def get_jobs(job, location, experience):

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 20,
        "what": job,
        "where": location
    }

    try:

        response = requests.get(url, params=params)

        data = response.json()

        jobs = []

        if "results" not in data:
            return []

        for item in data["results"]:

            jobs.append({
                "title": item.get("title", "N/A"),
                "company": item.get("company", {}).get("display_name", "N/A"),
                "location": item.get("location", {}).get("display_name", "N/A"),
                "description": item.get("description", ""),
                "redirect_url": item.get("redirect_url", "#")
            })

        return jobs

    except Exception as e:
        print(e)
        return []