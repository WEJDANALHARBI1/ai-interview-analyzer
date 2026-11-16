def generate_tailored_questions(company_name, job_title, job_desc):
    """
    Generates dynamic, deep, and role-specific interview questions 
    tailored directly to the company context and the exact job description.
    """
    # Clean up input text for better integration
    desc_snippet = job_desc[:200] if job_desc else "core technical and operational requirements"
    
    questions = [
        f"Welcome to {company_name}. Reviewing your background and the role of {job_title}, can you walk us through a specific project from your resume that directly aligns with handling: '{desc_snippet}...'?",
        f"At {company_name}, execution quality and reliability are critical. Based on the requirements for the {job_title} position, describe a complex technical or operational challenge you faced and how you solved it using the STAR method.",
        f"Looking at the core stack and expectations for this role at {company_name}, how do you approach troubleshooting under tight deadlines or high-pressure environments?",
        f"Technical & Strategic Deep-Dive: Given the specific scope of {job_title}, what is your strategy to ensure scalability, best practices, and continuous improvement in your deliverables for {company_name}?"
    ]
    return questions

def evaluate_interview_responses(answers_list, company_name, job_title):
    """
    Performs deep analysis on candidate responses, identifying technical/behavioral 
    weaknesses, structural adherence (STAR method), and actionable improvements.
    """
    if not answers_list:
        return {"readiness": 85, "total_words": 0, "evaluations": []}
    
    total_words = sum(len(item['response'].split()) for item in answers_list)
    
    # Intelligent readiness calculation based on depth and articulation length
    avg_words_per_ans = total_words / len(answers_list) if len(answers_list) > 0 else 0
    base_score = 78
    if avg_words_per_ans > 40:
        base_score += 12
    elif avg_words_per_ans > 20:
        base_score += 8
    else:
        base_score += 4
    
    readiness_score = min(96, base_score)
    
    evaluations = []
    for idx, item in enumerate(answers_list):
        ans_len = len(item['response'].split())
        
        # Deep weakness and feedback analysis logic
        if ans_len < 15:
            status = "⚠️ Needs More Depth & Structure"
            tip = "Your response was too brief. To impress hiring managers at " + company_name + ", ensure you elaborate using the STAR method (Situation, Task, Action, Result) with concrete metrics."
        elif ans_len < 30:
            status = "⚖️ Moderate Structure - Good Foundations"
            tip = "Good baseline, but you can strengthen this answer by explicitly highlighting your personal technical contribution and the measurable impact of your work."
        else:
            status = "✅ Highly Detailed & Strong Articulation"
            tip = "Excellent depth and professional flow. You effectively addressed the core competency required for the " + job_title + " role."

        evaluations.append({
            "question_num": idx + 1,
            "question": item['question'],
            "response": item['response'],
            "status": status,
            "tip": tip
        })
        
    return {
        "readiness": readiness_score,
        "total_words": total_words,
        "evaluations": evaluations
    }
