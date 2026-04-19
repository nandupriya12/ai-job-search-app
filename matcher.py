from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(resume_text, jobs):

    job_texts = [
        job['title'] + " " + job['company'] + " " + job.get('description', "")
        for job in jobs
    ]

    documents = [resume_text] + job_texts

    tfidf = TfidfVectorizer().fit_transform(documents)

    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    for i, job in enumerate(jobs):
        job['match_score'] = round(scores[i] * 100, 2)

    return sorted(jobs, key=lambda x: x['match_score'], reverse=True)