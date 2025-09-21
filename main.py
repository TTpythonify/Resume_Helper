import streamlit as st
from jobs import fetch_adzuna_jobs
from logic import extract_job_keywords

def run_resume_assistant():
    # Page config
    st.set_page_config(
        page_title="AI Resume Assistant",
        page_icon="📄",
        layout="centered"
    )

    # Styling
    st.markdown("""
    <style>
        .main {padding: 2rem; max-width: 800px; margin: 0 auto;}
        .title {text-align: center; color: #1f2937; font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem;}
        .subtitle {text-align: center; color: #6b7280; font-size: 1.2rem; margin-bottom: 3rem;}
        .upload-section, .job-section {background: #f8fafc; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid #e5e7eb;}
        .section-title {font-size: 1.3rem; font-weight: 600; color: #374151; margin-bottom: 1rem;}
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 1rem 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="title">📄 AI Resume Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload your resume and job description to get started</p>', unsafe_allow_html=True)

    # Upload CV section
    st.markdown('<div class="section-title">📁 Upload Resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Choose your CV file", type=["pdf", "docx"])

    # Job description section
    st.markdown('<div class="section-title">💼 Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste the job description here",
        height=150,
        placeholder="Enter the complete job description..."
    )

    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search_button = st.button("🔍 Analyze Match", use_container_width=True)

    # Handle search button click
    if search_button:
        if not resume_file or not job_description.strip():
            st.error("Please upload a resume and enter a job description.")
        else:
            st.session_state.show_results = True
            st.success("✅ Analysis complete!")

            # 1. Extract keywords from job description
            keywords = extract_job_keywords(job_description)
            title = keywords.get('job_title', '')
            skills = keywords.get('skills', [])
            query = f"{title} {' '.join(skills)}"

            # 2. Ensure locations is a list
            locations = keywords.get('location', [])
            if isinstance(locations, str):
                locations = [locations]
            elif not locations:
                # fallback locations if GPT fails
                locations = ['Dublin', 'Cork', 'Sligo']

            # 3. Fetch jobs from Adzuna
            all_results = []
            for loc in locations:
                results = fetch_adzuna_jobs(query, loc)
                all_results.extend(results)

            # 4. Display results nicely
            for i, job in enumerate(all_results, start=1):
                st.markdown(f"**{i}. {job.get('title', 'No title')}**")
                st.markdown(f"Company: {job.get('company', {}).get('display_name', 'Unknown')}")
                st.markdown(f"Location: {job.get('location', {}).get('display_name', 'Unknown')}")
                st.markdown(f"Salary: {job.get('salary_min', 'N/A')} - {job.get('salary_max', 'N/A')}")
                st.markdown(f"[Apply here]({job.get('redirect_url', '#')})")
                st.markdown("---")  # separator


# Run the function if this file is executed
if __name__ == "__main__":
    run_resume_assistant()
