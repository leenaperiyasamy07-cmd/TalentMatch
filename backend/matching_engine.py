from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def calculate_match_score(resume_text, job_description, resume_features=None, jd_features=None):
    import math
    if not resume_text.strip() or not job_description.strip():
        return 0.0
        
    # 1. Semantic Score (Advanced TF-IDF)
    # We use ngram_range up to 3 to capture "AWS Certified Solutions"
    clean_resume = re.sub(r'[•\d+]', ' ', resume_text)
    clean_jd = re.sub(r'[•\d+]', ' ', job_description)
    
    documents = [clean_resume, clean_jd]
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), min_df=1)
    
    semantic_score = 0.0
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarity = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        
        # Logarithmic Scaling: Maps 0.05 similarity to ~50, 0.2 to ~85
        if similarity > 0:
            semantic_score = min(100.0, 50 + (math.log10(similarity * 20 + 1) * 45))
        else:
            semantic_score = 0.0
    except:
        semantic_score = 0.0
        
    # 2. Multi-Factor Feature Match
    feature_points = 0
    total_weights = 0
    
    if resume_features and jd_features:
        # A. Skills Match (40% weight)
        r_skills = set(s.lower() for s in resume_features.get("skills", []))
        j_skills = set(s.lower() for s in jd_features.get("skills", []))
        if j_skills:
            skill_pct = (len(r_skills.intersection(j_skills)) / len(j_skills)) * 100
            feature_points += (skill_pct * 0.4)
            total_weights += 0.4
            
        # B. Certifications Match (30% weight - MASSIVE SIGNAL)
        # If JD asks for certs, and resume has them, huge boost
        r_certs = set(c.lower() for c in resume_features.get("certifications", []))
        j_certs = set(c.lower() for c in jd_features.get("certifications", []))
        if j_certs:
            cert_match = (len(r_certs.intersection(j_certs)) / len(j_certs)) * 100
            feature_points += (cert_match * 0.3)
            total_weights += 0.3
        elif r_certs: # General boost for having certs in an IT field
            feature_points += 20 * 0.3 # Small general boost
            total_weights += 0.3
            
        # C. Experience & Seniority (30% weight)
        r_years = resume_features.get("experience_years", 0)
        j_years = jd_features.get("experience_years", 0)
        if r_years >= j_years and j_years > 0:
            feature_points += (100 * 0.3)
        elif r_years > 0:
            feature_points += (min(100, (r_years/5)*100) * 0.3)
        total_weights += 0.3
        
    # Final Weighted Calculation
    # 50% Deep Features (Certs/Skills/Exp) + 50% Semantic (Writing Style/Context)
    keyword_score = 0.0
    if total_weights > 0:
        keyword_score = feature_points / total_weights
        final_score = (semantic_score * 0.5) + (keyword_score * 0.5)
    else:
        final_score = semantic_score
        
    # Quality Seal: If a Senior with Certs matches a JD, they must be 90+
    if resume_features and jd_features:
        if resume_features.get("seniority") == "Senior" and len(resume_features.get("certifications")) > 0:
            if keyword_score > 70:
                final_score = max(final_score, 92.0)

    # Prepare return data
    final_score = round(min(100.0, final_score), 2)
    
    return {
        "final_score": final_score,
        "breakdown": {
            "semantic_score": round(semantic_score, 2),
            "feature_score": round(keyword_score, 2),
            "skills_match": round(skill_pct, 2) if 'skill_pct' in locals() else 0,
            "cert_match": round(cert_match, 2) if 'cert_match' in locals() else (20 if 'r_certs' in locals() and r_certs else 0),
            "exp_match": round((100 if r_years >= j_years else min(100, (r_years/5)*100)) if 'r_years' in locals() else 0, 2)
        }
    }

def identify_missing_skills(resume_skills, job_skills):
    # Case insensitive comparison
    resume_skills_lower = [s.lower() for s in resume_skills]
    missing = [s for s in job_skills if s.lower() not in resume_skills_lower]
    return missing
