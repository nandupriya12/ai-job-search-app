import streamlit as st
import pandas as pd
from scraper import get_jobs
from resume_parser import extract_text
from matcher import match_jobs

st.set_page_config(
    page_title="Smart AI Job Search",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Smart AI Job Search App")

st.markdown("""
<style>

.block-container{
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
}

.stTextInput > div > div > input {
    border-radius: 12px;
    height: 50px;
    font-size: 16px;
}

.stSelectbox > div > div {
    border-radius: 12px;
}

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    background-color: #2563eb;
    color: white;
    border: none;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

[data-testid="stMetric"] {
    background-color: #111827;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    job = st.text_input(
        "Enter job role",
        placeholder="python developer"
    )

with col2:
    location = st.text_input(
        "Enter location",
        placeholder="london"
    )

experience = st.selectbox(
    "Experience Level",
    ["Any", "Junior", "Mid", "Senior"]
)

sort_option = st.selectbox(
    "Sort By",
    ["Best Match", "Highest Score"]
)

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

if st.button("Search Jobs"):

    if not job or not location:
        st.warning("Please enter role and location")
        st.stop()

    with st.spinner("Searching jobs..."):

        jobs = get_jobs(job, location, experience)

    if not jobs:
        st.error("No jobs found")
        st.stop()

    if uploaded_file:

        resume_text = extract_text(uploaded_file)

        jobs = match_jobs(resume_text, jobs)

        if sort_option == "Highest Score":
            jobs = sorted(
                jobs,
                key=lambda x: x.get("match_score", 0),
                reverse=True
            )

        st.success("Resume analyzed successfully")

    st.subheader("Top Job Matches")

    top_score = max(
        [job.get("match_score", 0) for job in jobs]
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Jobs Found", len(jobs))
    c2.metric("Best Match", f"{top_score:.2f}%")
    c3.metric("Location", location.title())

    st.divider()

    for i, j in enumerate(jobs):

        score = j.get("match_score", 0)

        if score >= 15:
            st.success("⭐ Excellent Match")

        elif score >= 8:
            st.info("👍 Good Match")

        else:
            st.warning("⚠ Low Match")

        st.markdown(
            f"""
            <div style="
                background-color:#111827;
                padding:25px;
                border-radius:18px;
                margin-bottom:25px;
                border:1px solid #1f2937;
            ">

            <h2 style="margin-bottom:15px;">
            {j['title']}
            </h2>

            <p style="font-size:18px;">
            🏢 <b>{j['company']}</b>
            </p>

            <p>
            📍 {j['location']}
            </p>

            <p>
            🔥 Match Score: <b>{score:.2f}%</b>
            </p>

            <p>
            🧠 Skills: {', '.join(j.get('matched_skills', []))}
            </p>

            <a href="{j['redirect_url']}" target="_blank">
                Apply Here →
            </a>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

    df = pd.DataFrame(jobs)

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Jobs CSV",
        csv,
        "jobs.csv",
        "text/csv"
    )