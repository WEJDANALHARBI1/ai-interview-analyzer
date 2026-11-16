import os
import openai

def get_openai_client(api_key):
    """Initializes and returns the OpenAI client with the provided API key."""
    if not api_key:
        return None
    return openai.OpenAI(api_key=api_key)

def generate_ai_questions(client, company_name, job_title, job_desc, cv_text):
    """
    Uses OpenAI GPT-4o to generate deep, tailored, and unique interview questions
    based on the candidate's CV, company profile, and job description.
    """
    if not client:
        # Fallback if no API key is provided yet
        return [
            f"Welcome to {company_name}. Can you walk us through your key experience relevant to the {job_title} role?",
            "Describe a complex technical challenge you faced and how you resolved it using the STAR method.",
            "How do you handle tight deadlines and high-pressure situations in your team?",
            f"Given the requirements for {job_title}, what is your approach to ensuring scalability and quality?"
        ]

    prompt = f"""
    You are an expert technical interviewer and hiring manager at {company_name}.
    Target Role: {job_title}
    Job Description: {job_desc}
    Candidate Resume Summary: {cv_text[:1000]}

    Generate exactly 4 rigorous, unique, and highly targeted interview questions for this candidate applying for this specific role at {company_name}. 
    Make sure they cover:
    1. Introduction & resume alignment.
    2. Behavioral/STAR problem solving.
    3. Pressure/collaboration handling.
    4. Technical/Role-specific deep dive.
    
    Return ONLY the 4 questions separated by numbers (1., 2., 3., 4.). No extra fluff.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        questions = [q.strip() for q in content.split('\n') if q.strip() and q[0].isdigit()]
        cleaned = [q.split('.', 1)[1].strip() if '.' in q else q for q in questions]
        return cleaned[:4] if len(cleaned) >= 4 else questions[:4]
    except Exception as e:
        return [
            f"Error generating AI questions: {str(e)}. Please check your API key."
        ]

def evaluate_answer_with_ai(client, question, user_answer, company_name, job_title):
    """
    Uses OpenAI GPT-4o to deeply analyze a single candidate response, 
    detect weaknesses, evaluate STAR method adherence, and provide coaching tips.
    """
    if not client:
        return {
            "status": "✅ General Analysis",
            "tip": "Provide your OpenAI API key for deep AI-powered weakness detection and STAR coaching."
        }

    prompt = f"""
    You are an expert career coach and interviewer at {company_name} hiring for {job_title}.
    Question: {question}
    Candidate Answer: {user_answer}

    Evaluate this response thoroughly. Provide:
    1. Status: A short evaluation status starting with an emoji (e.g., "✅ Strong STAR Structure", "⚠️ Missing Quantifiable Results", "❌ Too Brief / Lacks Depth").
    2. Targeted Coaching & Weakness Correction: Specific, actionable feedback explaining what was weak, what was missing, and how the candidate can phrase it better using the STAR method.

    Format your output strictly as:
    STATUS: [Your status here]
    TIP: [Your detailed coaching tip here]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content
        
        status = "✅ Analyzed"
        tip = content
        
        for line in content.split('\n'):
            if line.startswith("STATUS:"):
                status = line.replace("STATUS:", "").strip()
            elif line.startswith("TIP:"):
                tip = line.replace("TIP:", "").strip()
                
        return {"status": status, "tip": tip}
    except Exception as e:
        return {
            "status": "⚠️ Evaluation Error",
            "tip": f"Could not process AI evaluation due to error: {str(e)}"
        }
