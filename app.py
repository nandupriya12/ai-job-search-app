import streamlit as st
from scraper import get_jobs
from resume_parser import extract_text
from matcher import match_jobs

st.title("💼 Smart AI Job Search App")

# INPUTS
job = st.text_input("Enter job role (e.g., teacher, developer, designer)")
location = st.text_input("Enter location (India / USA / Remote)")

experience = st.selectbox(
    "Experience Level",
    ["Any", "Junior", "Mid", "Senior"]
)

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# SEARCH BUTTON
if st.button("Search"):

    st.write("🔍 Searching jobs...")

    jobs = get_jobs(job, location, experience)

    if uploaded_file:
        resume_text = extract_text(uploaded_file)
        st.write("✅ Resume uploaded successfully!")
        jobs = match_jobs(resume_text, jobs)

    st.write("### Jobs Found:")

    for i, j in enumerate(jobs):

        if i == 0:
            st.success("⭐ Best Match")
        elif i < 3:
            st.info("👍 Good Match")

        if 'match_score' in j:
            st.write(f"🔥 Match Score: {j['match_score']}%")

        # 💼 Freelance tag
        if j['company'] in ["Self-employed", "Private Clients"]:
            st.write("💼 Freelance Opportunity")

        # Job card
        st.markdown(
            f"""
            <div style="
                padding:15px;
                border-radius:10px;
                background-color:#1e1e1e;
                color:white;
                margin-bottom:10px;
                border:1px solid #ddd;
            ">
                <h4>{j['title']}</h4>
                <p><b>{j['company']}</b></p>
                <p>{j['location']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )