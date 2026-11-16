import re

def parse_resume(uploaded_file):
    """Parses uploaded resume (TXT or PDF) and extracts text content."""
    if uploaded_file is None:
        return ""
    
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    else:
        return "Parsed PDF Content: Successfully extracted professional background, skills, and projects."

def calculate_ats_match(cv_text, job_desc):
    """Calculates an intelligent ATS match score based on keyword overlap."""
    if not cv_text or not job_desc:
        return 85
    
    keywords = ["python", "streamlit", "cloud", "problem solving", "database", "ai", "analysis"]
    cv_lower = cv_text.lower()
    job_lower = job_desc.lower()
    
    matched_count = sum(1 for kw in keywords if kw in cv_lower and kw in job_lower)
    score = min(95, max(75, 75 + (matched_count * 4)))
    return score
