from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn
import asyncio

from utils import extract_text
from nlp_processor import SkillExtractor
from matching_engine import calculate_match_score, identify_missing_skills
from roadmap_generator import generate_roadmap
from job_profiles import recommend_jobs
from career_trajectory import predict_career_trajectory, simulate_skill_evolution

app = FastAPI(title="SkillPath AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

extractor = SkillExtractor()

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(None)
):
    # 1. Read file
    content = await resume.read()
    resume_text = extract_text(content, resume.filename)
    
    # 2. Extract Candidate features (Deep Analysis)
    candidate_features = extractor.extract_features(resume_text)
    candidate_skills = candidate_features["skills"]
    
    # 3. Automatic Job Recommendation
    best_fits = recommend_jobs(candidate_skills, job_description or "")

    # 4. Handle Case where JD is empty - Automatic Analysis
    target_jd = job_description
    if not target_jd or target_jd.strip() == "":
        if best_fits:
            top_fit = best_fits[0]
            target_jd = f"Role: {top_fit['role']}. Required Skills: {', '.join(top_fit['matched_skills'] + top_fit['missing_skills'])}"
        else:
            target_jd = "No specific job requirements provided."

    # 5. Extract JD features
    jd_features = extractor.extract_features(target_jd)
    jd_skills = jd_features["skills"]
    
    # 6. Calculate Score using Deep Features
    score = calculate_match_score(resume_text, target_jd, candidate_features, jd_features)
    
    # 7. Identify Gaps
    missing_skills = identify_missing_skills(candidate_skills, jd_skills)
    
    # 8. Generate Roadmap
    roadmap = generate_roadmap(missing_skills)
    
    # For each best fit, generate a side-roadmap
    for fit in best_fits:
        fit["roadmap"] = generate_roadmap(fit["missing_skills"])

    # 9. Career Trajectory
    trajectories = predict_career_trajectory(candidate_skills)
    
    return {
        "candidate_name": resume.filename.split(".")[0],
        "score": score,
        "found_skills": candidate_skills,
        "required_skills": jd_skills,
        "missing_skills": missing_skills,
        "features": candidate_features,
        "roadmap": roadmap,
        "best_fits": best_fits,
        "career_trajectories": trajectories,
        "market_insights": extractor.get_market_insights(candidate_features["seniority"], candidate_skills),
        "radar_data": extractor.get_radar_data(candidate_skills, jd_skills),
        "interview_prep": extractor.generate_interview_prep(missing_skills),
        "resume_suggestions": extractor.generate_resume_suggestions(candidate_skills, missing_skills),
        "auto_analyzed": not bool(job_description),
        "resume_text": resume_text,
        "jd_text": target_jd
    }

@app.post("/hr/bulk-upload")
async def hr_bulk_upload(
    resumes: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    jd_features = extractor.extract_features(job_description)
    jd_skills = jd_features["skills"]
    
    results = []
    
    for resume in resumes:
        content = await resume.read()
        text = extract_text(content, resume.filename)
        candidate_features = extractor.extract_features(text)
        candidate_skills = candidate_features["skills"]
        
        # Calculate job-specific matches
        matched_skills = [s for s in candidate_skills if any(s.lower() == js.lower() for js in jd_skills)]
        total_jd = len(jd_skills) if jd_skills else 1
        skill_match_pct = round((len(matched_skills) / total_jd) * 100, 2)
        
        # Calculate scores using Deep Features
        score = calculate_match_score(text, job_description, candidate_features, jd_features)
        missing = identify_missing_skills(candidate_skills, jd_skills)
        
        # Potential Score: How much can they improve FOR THIS JOB specifically
        # We simulate adding the detected missing skills (capped at 5 skills for realism)
        potential_gain = 0
        if missing:
            top_missing = missing[:3]
            simulated_text = text + " " + " ".join(top_missing)
            simulated_features = extractor.extract_features(simulated_text)
            future_score = calculate_match_score(simulated_text, job_description, simulated_features, jd_features)
            potential_gain = round(future_score - score, 2)
            
        # Overall Match remains the primary ranking metric
        # Potential Score shows how "reachable" this job is for them
        results.append({
            "candidate_name": resume.filename.split(".")[0],
            "overall_match": score,
            "skill_match": min(100.0, skill_match_pct),
            "potential_score": max(0, potential_gain),
            "found_skills": matched_skills if matched_skills else ["No JD Overlap"],
            "missing_skills": missing
        })
        
    # Rank candidates by technical skill_match as requested
    results.sort(key=lambda x: x["skill_match"], reverse=True)
    
    # Add ranks based on skill overlap
    for idx, res in enumerate(results):
        res["rank"] = idx + 1
        
    return {
        "job_description_skills": jd_skills,
        "ranked_candidates": results
    }

@app.post("/student/simulate")
async def simulate_evolution(
    payload: Dict[str, Any] = Body(...)
):
    current_text = payload.get("resume_text", "")
    jd_text = payload.get("jd_text", "")
    
    # Simulate addition of skills into text
    potential_skills = payload.get("potential_skills", [])
    simulated_text = current_text + " " + " ".join(potential_skills)
    
    # Extract features for both
    res_features = extractor.extract_features(simulated_text)
    jd_features = extractor.extract_features(jd_text)
    
    # Calculate Score using Deep Features
    score = calculate_match_score(simulated_text, jd_text, res_features, jd_features)
    
    # Recalculate current for comparison
    curr_res_features = extractor.extract_features(current_text)
    current_score = calculate_match_score(current_text, jd_text, curr_res_features, jd_features)
    
    return {
        "current_score": current_score,
        "future_score": score,
        "improvement": round(score - current_score, 2),
        "tested_skills": potential_skills
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
