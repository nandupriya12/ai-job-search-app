def extract_text(uploaded_file):
    import pdfplumber

    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text.lower()


# ✅ NEW FUNCTION (IMPORTANT)
def extract_skills(text):
    skills_list = [
        "python", "java", "c++", "sql",
        "machine learning", "data science",
        "html", "css", "javascript",
        "react", "node", "django",
        "flask", "nlp", "deep learning",
        "communication", "teaching",
        "kannada", "english"
    ]

    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills