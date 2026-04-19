def extract_text(uploaded_file):
    import pdfplumber

    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # CLEAN SKILLS
    words = text.lower().split()

    stopwords = [
        "and", "the", "with", "for", "from", "this", "that",
        "anjali", "reddy", "india", "email", "phone",
        "experience", "professional", "summary", "through",
        "student", "students"
    ]

    skills = [w for w in words if len(w) > 3 and w not in stopwords]

    return " ".join(skills)