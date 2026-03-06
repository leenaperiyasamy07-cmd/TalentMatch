import re

# List of common technical skills
SKILLS_DB = [
    # Languages
    "Python", "Java", "JavaScript", "C++", "C#", "SQL", "HTML", "CSS", "PHP", "Go", "Rust", "Kotlin", "Swift", "Ruby", "TypeScript", "Scala", "R", "MATLAB", "Perl",
    # Frontend
    "React", "Angular", "Vue", "Svelte", "Next.js", "Tailwind", "Bootstrap", "Redux", "JQuery", "SASS", "LESS", "Webpack", "Vite", "Canvas", "WebGL",
    # Backend & Frameworks
    "Node.js", "Express", "Flask", "FastAPI", "Django", "Spring Boot", "Laravel", "Rails", "ASP.NET", "NestJS", "Hibernate", "Entity Framework",
    # Databases
    "PostgreSQL", "MongoDB", "MySQL", "Oracle", "SQL Server", "Redis", "Elasticsearch", "Cassandra", "DynamoDB", "Firebase", "MariaDB", "SQLite",
    # Cloud & DevOps
    "AWS", "Azure", "Docker", "Kubernetes", "Git", "GitHub", "Jenkins", "Terraform", "Ansible", "CircleCI", "Travis CI", "Nginx", "Apache", "GCP", "Heroku", "Vercel", "DigitalOcean",
    # AI/ML/Data
    "Machine Learning", "Data Science", "Deep Learning", "NLP", "Scikit-learn", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Tableau", "Power BI", "Keras", "Matplotlib", "Seaborn", "PySpark", "Hadoop", "Spark", "Kafka", "Data Engineering", "Computer Vision",
    # Design & Tools
    "Figma", "Adobe XD", "Photoshop", "Illustrator", "Sketch", "AutoCAD", "ANSYS", "Mathematica", "Ultimaker Cura", "Unity", "Unreal Engine", "Blender",
    # Mobile
    "React Native", "Flutter", "Ionic", "Xamarin", "Objective-C",
    # Other / Concepts
    "REST API", "GraphQL", "Microservices", "Serverless", "Unit Testing", "TDD", "Agile", "Scrum", "Jira", "Linux", "Unix", "Cybersecurity", "Blockchain", "Solidity"
]

class SkillExtractor:
    def __init__(self):
        # We'll use a simple but effective regex-based keyword matcher
        # This avoids the Pydantic/spaCy compatibility issues on Python 3.14
        self.skills_db = SKILLS_DB

    def extract_features(self, text):
        results = {
            "skills": self.extract_skills(text),
            "certifications": [],
            "experience_years": 0,
            "seniority": "Junior"
        }
        
        # 1. Certifications extraction (Higher Weight)
        cert_patterns = [
            r"CCNA", r"CCNP", r"CCIE", r"Security\+", r"Network\+", r"A\+", r"Server\+",
            r"AWS Certified", r"Solutions Architect", r"Azure Certified", r"CISSP", 
            r"CISA", r"CISM", r"PMP", r"ITIL", r"VCP", r"CompTIA", r"Cisco Certified",
            r"Google Cloud Certified", r"Certified Ethical Hacker", r"CEH"
        ]
        for pattern in cert_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                results["certifications"].append(pattern.replace("\\", ""))
        
        # 2. Years of Experience detection (Broader Patterns)
        patterns = [
            r"(\d+)\+?\s*years?\s*of?\s*experience",
            r"(\d+)\+?\s*years?\s*in\s*IT",
            r"experience:?\s*(\d+)\+?\s*years?",
            r"(\d+)\+?\s*years?\s*professional\s*experience"
        ]
        
        max_years = 0
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                val = int(match.group(1))
                if val > max_years:
                    max_years = val
        
        results["experience_years"] = max_years
            
        # 3. Seniority Detection
        if results["experience_years"] >= 7 or re.search(r"Principal|Director|Architect", text, re.IGNORECASE):
            results["seniority"] = "Expert / Architect"
        elif results["experience_years"] >= 5 or re.search(r"Senior|Lead|Manager", text, re.IGNORECASE):
            results["seniority"] = "Senior"
        elif results["experience_years"] >= 3:
            results["seniority"] = "Mid-Level"
            
        return results

    def generate_interview_prep(self, missing_skills):
        prep = []
        for skill in missing_skills[:3]:
            prep.append({
                "skill": skill,
                "question": f"Can you describe a time where you had to quickly learn {skill} to solve a problem, or how you would approach a project requiring it?",
                "tip": f"Be honest about being in the learning phase, but emphasize your foundational knowledge in related areas and your speed of acquisition."
            })
        
        # Add a general behavioral one
        prep.append({
            "skill": "Growth Mindset",
            "question": "We noticed some technical gaps compared to our ideal profile. How do you plan to bridge these in your first 90 days?",
            "tip": "Showcase your proactive learning plan. Mention specific certifications or courses you've already identified."
        })
        return prep

    def generate_resume_suggestions(self, found_skills, missing_skills):
        suggestions = []
        for skill in found_skills[:2]:
            suggestions.append(f"Strengthen your {skill} section by quantifying achievements (e.g., 'Optimized {skill} workflows reducing latency by 20%').")
        
        for skill in missing_skills[:2]:
            suggestions.append(f"Consider adding a 'Currently Learning' or 'Projects' section to showcase your emerging expertise in {skill}.")
            
        return suggestions

    def get_market_insights(self, seniority, skills):
        # Simulated Market Insights based on Role/Skills
        salary_ranges = {
            "Junior": "$50k - $80k",
            "Mid-Level": "$90k - $130k",
            "Senior": "$140k - $190k",
            "Expert / Architect": "$200k - $280k"
        }
        
        demand = "Medium"
        if any(s.lower() in ["aws", "cloud", "security", "ai", "machine learning"] for s in skills):
            demand = "Very High"
        elif len(skills) > 10:
            demand = "High"
            
        return {
            "estimated_salary": salary_ranges.get(seniority, "$60k+"),
            "market_demand": demand,
            "remote_friendliness": "85%" if any(s.lower() in ["javascript", "react", "python", "cloud"] for s in skills) else "60%"
        }

    def get_radar_data(self, resume_skills, jd_skills):
        categories = ["Cloud", "Backend", "Frontend", "Data", "DevOps"]
        cat_map = {
            "Cloud": ["aws", "azure", "gcp", "cloud", "terrafom"],
            "Backend": ["python", "java", "node.js", "sql", "rest api", "django", "express"],
            "Frontend": ["react", "javascript", "html", "css", "vue", "angular", "ui", "ux"],
            "Data": ["data science", "machine learning", "pandas", "numpy", "sql", "tableau"],
            "DevOps": ["docker", "kubernetes", "jenkins", "git", "linux", "ansible"]
        }
        
        res_scores = []
        jd_scores = []
        
        for cat in categories:
            keywords = cat_map[cat]
            res_val = len([s for s in resume_skills if s.lower() in keywords])
            jd_val = len([s for s in jd_skills if s.lower() in keywords])
            
            # Normalize to 10-point scale for chart
            res_scores.append(min(10, res_val * 2.5))
            jd_scores.append(min(10, jd_val * 2.5))
            
        return {
            "labels": categories,
            "resume_values": res_scores,
            "jd_values": jd_scores
        }

    def extract_skills(self, text):
        found_skills = set()
        text_lower = text.lower()
        
        # Mapping of synonyms to Ensure "Fuzzy" matching
        synonyms = {
            "Cybersecurity": ["cyber security", "infosec", "information security", "security protocols"],
            "System Administration": ["sysadmin", "it infrastructure", "server management"],
            "Cloud Computing": ["aws", "azure", "gcp", "cloud migration", "cloud operations"],
            "Network Configuration": ["cisco", "ccna", "networking", "routing", "switching"],
            "Troubleshooting": ["help desk", "technical support", "it support"],
            "Data Science": ["machine learning", "ai", "deep learning", "predictive modeling"]
        }
        
        # 1. Direct Keyword Match
        for skill in self.skills_db:
            pattern = rf"(?<![a-zA-Z0-9]){re.escape(skill)}(?![a-zA-Z0-9])"
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.add(skill)
                
        # 2. Synonym Logic
        for main_skill, alternatives in synonyms.items():
            for alt in alternatives:
                if alt in text_lower:
                    found_skills.add(main_skill)
                    
        return list(found_skills)
