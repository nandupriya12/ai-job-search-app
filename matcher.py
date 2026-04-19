from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import extract_skills   # import skills function

def match_jobs(resume_text, jobs):

    # ✅ Extract skills from resume
    resume_skills = extract_skills(resume_text)

    # ✅ Prepare job texts
    job_texts = [
        job['title'] + " " + job['company'] + " " + job.get('description', "")
        for job in jobs
    ]

    # ✅ Combine resume + jobs
    documents = [resume_text] + job_texts

    # ✅ TF-IDF Vectorization
    tfidf = TfidfVectorizer().fit_transform(documents)

    # ✅ Similarity calculation
    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    # ✅ Assign scores + match explanation
    for i, job in enumerate(jobs):
        job['match_score'] = round(scores[i] * 100, 2)

        # 🔥 Match explanation (Week 4 requirement)
        job_text = (job['title'] + " " + job.get('description', "")).lower()
        common_skills = [skill for skill in resume_skills if skill in job_text]

        job['matched_skills'] = common_skills

    # ✅ Sort jobs by best match
    jobs = sorted(jobs, key=lambda x: x['match_score'], reverse=True)

    return jobs