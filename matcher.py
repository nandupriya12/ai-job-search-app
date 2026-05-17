from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_skills(text):

    skills_list = [
        "python",
        "java",
        "sql",
        "machine learning",
        "data science",
        "power bi",
        "excel",
        "tableau",
        "django",
        "flask",
        "react",
        "javascript",
        "communication"
    ]

    found = []

    for skill in skills_list:

        if skill.lower() in text.lower():
            found.append(skill)

    return found


def match_jobs(resume_text, jobs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    resume_chunks = splitter.split_text(resume_text)

    resume_processed = " ".join(resume_chunks)

    resume_skills = extract_skills(resume_processed)

    for job in jobs:

        job_text = (
            job["title"] + " " +
            job["description"]
        )

        tfidf = TfidfVectorizer()

        tfidf_matrix = tfidf.fit_transform([
            resume_processed,
            job_text
        ])

        score = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        matched = []

        for skill in resume_skills:

            if skill.lower() in job_text.lower():
                matched.append(skill)

        job["match_score"] = round(score * 100, 2)

        job["matched_skills"] = matched

    jobs = sorted(
        jobs,
        key=lambda x: x["match_score"],
        reverse=True
    )

    return jobs