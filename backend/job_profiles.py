JOB_PROFILES = [
    {
        "role": "Full Stack Developer",
        "skills": ["JavaScript", "React", "Node.js", "Express", "MongoDB", "HTML", "CSS", "SQL", "Git"]
    },
    {
        "role": "Data Scientist",
        "skills": ["Python", "Machine Learning", "Data Science", "Pandas", "NumPy", "Scikit-learn", "SQL", "TensorFlow"]
    },
    {
        "role": "DevOps Engineer",
        "skills": ["AWS", "Docker", "Kubernetes", "Jenkins", "Terraform", "Ansible", "Linux", "Git", "Nginx"]
    },
    {
        "role": "Frontend Developer",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Vue", "Angular", "Tailwind", "Figma", "Redux"]
    },
    {
        "role": "Backend Developer",
        "skills": ["Python", "Java", "Node.js", "Express", "Django", "Flask", "PostgreSQL", "Redis", "Rest API"]
    },
    {
        "role": "Data Engineer",
        "skills": ["SQL", "PySpark", "Hadoop", "Spark", "Kafka", "Data Engineering", "AWS", "Scala"]
    },
    {
        "role": "AI/NLP Engineer",
        "skills": ["Python", "NLP", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Scikit-learn"]
    },
    {
        "role": "Mechanical/Design Engineer",
        "skills": ["AutoCAD", "ANSYS", "Mathematica", "Ultimaker Cura", "Mathematica", "SolidWorks"]
    }
]

def recommend_jobs(candidate_skills, job_description=""):
    recommendations = []
    candidate_skills_lower = [s.lower() for s in candidate_skills]
    job_description_lower = job_description.lower()
    
    for profile in JOB_PROFILES:
        # If user provided a specific JD, check if this profile matches the context
        # We check if the role name or any of its skills appear in the JD
        is_relevant = True
        if job_description and len(job_description) > 5:
            # Check if role name or keywords in description
            role_keywords = profile["role"].lower().split()
            role_match = any(word in job_description_lower for word in role_keywords if len(word) > 2)
            
            # Or if major skills are requested in JD
            profile_skills_lower = [s.lower() for s in profile["skills"]]
            skill_match = any(skill in job_description_lower for skill in profile_skills_lower[:3])
            
            is_relevant = role_match or skill_match

        if not is_relevant:
            continue

        matches = [s for s in profile["skills"] if s.lower() in candidate_skills_lower]
        missing = [s for s in profile["skills"] if s.lower() not in candidate_skills_lower]
        
        score = round((len(matches) / len(profile["skills"])) * 100, 2)
        
        recommendations.append({
            "role": profile["role"],
            "score": score,
            "matched_skills": matches,
            "missing_skills": missing
        })
    
    # Sort by score descending
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    # If we filtered and found nothing relevant, return the general top fits
    if not recommendations and job_description:
        return recommend_jobs(candidate_skills, "")

    return recommendations[:3]
