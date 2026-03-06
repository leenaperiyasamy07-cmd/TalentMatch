-- Database Schema for Intelligent Resume Screening
-- You can use this with MySQL or PostgreSQL

CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    resume_path VARCHAR(500),
    extracted_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    required_skills TEXT, -- Comma separated or JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    job_id INT,
    match_score DECIMAL(5, 2),
    found_skills TEXT,
    missing_skills TEXT,
    roadmap_json JSON,
    FOREIGN KEY (candidate_id) REFERENCES candidates (id),
    FOREIGN KEY (job_id) REFERENCES jobs (id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);