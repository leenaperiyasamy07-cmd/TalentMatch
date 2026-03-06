def predict_career_trajectory(current_skills):
    skills_lower = [s.lower() for s in current_skills]
    
    trajectories = []
    
    # 1. Backend / Fullstack path
    if any(s in skills_lower for s in ['java', 'python', 'node.js', 'c#', 'php', 'go']):
        path = {
            "possible_career": "Backend Developer",
            "progression": [
                {"stage": "Junior Backend Developer", "focus": "Core Language, Basic APIs"},
                {"stage": "Mid-Level Backend Engineer", "focus": "Microservices, Databases, Caching"},
                {"stage": "Senior System Architect", "focus": "System Design, Scalability, Cloud"}
            ],
            "recommended_additions": ["Docker", "Kubernetes", "System Design", "GraphQL"]
        }
        trajectories.append(path)
        
    # 2. Data / AI path
    if any(s in skills_lower for s in ['python', 'sql', 'machine learning', 'data science', 'pandas']):
        path = {
            "possible_career": "Data Scientist / Engineer",
            "progression": [
                {"stage": "Junior Data Analyst", "focus": "SQL, Data Cleaning, Basic Visualization"},
                {"stage": "Data Engineer / ML Engineer", "focus": "Data Pipelines, Model Deployment, Spark"},
                {"stage": "Lead AI Architect", "focus": "Enterprise AI Strategy, MLOps"}
            ],
            "recommended_additions": ["PySpark", "Airflow", "MLOps", "Deep Learning"]
        }
        trajectories.append(path)
        
    # 3. Frontend / UI path
    if any(s in skills_lower for s in ['javascript', 'react', 'html', 'css', 'vue', 'angular']):
        path = {
            "possible_career": "Frontend Developer",
            "progression": [
                {"stage": "Junior Frontend Developer", "focus": "HTML/CSS/JS, Basic React"},
                {"stage": "Senior Frontend Engineer", "focus": "State Management, Performance Optimization"},
                {"stage": "Frontend Architect / Staff Engineer", "focus": "Micro-frontends, Design Systems"}
            ],
            "recommended_additions": ["TypeScript", "Next.js", "Web Performance", "Testing"]
        }
        trajectories.append(path)

    # 4. DevOps / Cloud path
    if any(s in skills_lower for s in ['aws', 'docker', 'linux', 'kubernetes', 'jenkins', 'git']):
        path = {
            "possible_career": "DevOps Engineer",
            "progression": [
                {"stage": "DevOps Engineer", "focus": "CI/CD, Basic Cloud Services"},
                {"stage": "Site Reliability Engineer (SRE)", "focus": "Monitoring, Scaling, Infrastructure as Code"},
                {"stage": "Cloud Architect", "focus": "Multi-cloud Strategy, Enterprise Security"}
            ],
            "recommended_additions": ["Terraform", "Ansible", "Prometheus", "Service Mesh"]
        }
        trajectories.append(path)

    # Fallback if no strong match
    if not trajectories:
        trajectories.append({
            "possible_career": "Software Engineer",
            "progression": [
                {"stage": "Junior Engineer", "focus": "Core Programming Concepts"},
                {"stage": "Mid-Level Engineer", "focus": "Best Practices, Design Patterns"},
                {"stage": "Engineering Manager / Architect", "focus": "Leadership, High-Level Architecture"}
            ],
            "recommended_additions": ["Algorithms", "System Design", "Git", "Testing"]
        })
        
    return trajectories

def simulate_skill_evolution(current_text, current_skills, potential_skills, jd_text, jd_skills):
    from matching_engine import calculate_match_score
    
    # 1. Current Score (Weighted Semantic + Keyword)
    current_score = calculate_match_score(current_text, jd_text, current_skills, jd_skills)
    
    # 2. Simulate new state with potential skills
    # We append skills to text for TF-IDF and to list for keyword matching
    simulated_text = current_text + " " + " ".join(potential_skills)
    future_skills = list(set(current_skills + potential_skills))
    
    future_score = calculate_match_score(simulated_text, jd_text, future_skills, jd_skills)
    
    # Ensure score doesn't decrease and capped at 100
    future_score = max(current_score, min(100.0, future_score))
    
    return {
        "current_score": current_score,
        "future_score": future_score,
        "improvement": round(future_score - current_score, 2),
        "tested_skills": potential_skills
    }
