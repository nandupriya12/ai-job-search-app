from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import extract_skills


def match_jobs(resume_text, jobs):

    if not jobs:
        return []

    resume_skills = extract_skills(resume_text)

    job_texts = []

    for job in jobs:
        text = (
            str(job.get("title", "")) + " " +
            str(job.get("company", "")) + " " +
            str(job.get("description", ""))
        )

        job_texts.append(text)

    documents = [resume_text] + job_texts

    tfidf = TfidfVectorizer().fit_transform(documents)

    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    for i, job in enumerate(jobs):

        job['match_score'] = round(scores[i] * 100, 2)

        job_text = (
            job.get('title', '') + " " +
            job.get('description', '')
        ).lower()

        common_skills = [
            skill for skill in resume_skills
            if skill in job_text
        ]

        job['matched_skills'] = common_skills

    jobs = sorted(
        jobs,
        key=lambda x: x['match_score'],
        reverse=True
    )

    return jobs