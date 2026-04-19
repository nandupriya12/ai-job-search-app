def get_jobs(job, location, experience):
    return [
        {
            "title": f"{job.title()}",
            "company": "Google",
            "location": location,
            "description": f"{job} skills, teamwork, problem solving"
        },
        {
            "title": f"Senior {job.title()}",
            "company": "Microsoft",
            "location": location,
            "description": f"advanced {job}, leadership"
        },
        {
            "title": f"Personal {job.title()}",
            "company": "Self-employed",
            "location": location,
            "description": f"{job}, one-on-one teaching"
        },
        {
            "title": f"Home {job.title()}",
            "company": "Private Clients",
            "location": location,
            "description": f"{job}, tutoring, flexible schedule"
        }
    ]