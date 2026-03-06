// App State
const appState = {
    file: null,
    jd: '',
    results: null,
    hrFiles: [],
    hrResults: []
};

// DOM Elements - View Handling
const studentTab = document.getElementById('student-tab');
const resumeBuilderTab = document.getElementById('resume-builder-tab');
const hrTab = document.getElementById('hr-tab');
const backBtn = document.getElementById('back-btn');
const logoutBtn = document.getElementById('logout-btn');
const mainHeader = document.getElementById('main-header');

const landingView = document.getElementById('landing-view');
const studentView = document.getElementById('student-view');
const resumeBuilderView = document.getElementById('resume-builder-view');
const hrView = document.getElementById('hr-view');
const resultsView = document.getElementById('results-view');

const enterStudent = document.getElementById('enter-student');
const enterHR = document.getElementById('enter-hr');

const dropzone = document.getElementById('dropzone');
const resumeInput = document.getElementById('resume-input');
const fileNameDisplay = document.getElementById('file-name');
const form = document.getElementById('analyze-form');
const jdInput = document.getElementById('jd-input');
const nameInput = document.getElementById('name-input');

const roleSelectionArea = document.getElementById('role-selection-area');
const roleOptions = document.querySelectorAll('.role-chip');
const loader = document.getElementById('loader');

// DOM Elements - HR View
const hrDropzone = document.getElementById('hr-dropzone');
const hrResumeInput = document.getElementById('hr-resume-input');
const hrFileNameDisplay = document.getElementById('hr-file-name');
const hrForm = document.getElementById('hr-upload-form');
const hrJdInput = document.getElementById('hr-jd-input');
const rankingBody = document.getElementById('ranking-body');
const exportBtn = document.getElementById('export-btn');

// Other Sections
const trajectorySection = document.getElementById('trajectory-section');
const trajectoryContainer = document.getElementById('trajectory-container');

const simulatorSection = document.getElementById('simulator-section');
const simSkillsInput = document.getElementById('sim-skills-input');
const simBtn = document.getElementById('sim-btn');
const simResult = document.getElementById('sim-result');

let scoreChart = null;
let radarChart = null;

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
});

// Portal Entry Logic
enterStudent.addEventListener('click', () => {
    mainHeader.classList.remove('hidden');
    studentTab.classList.remove('hidden');
    resumeBuilderTab.classList.remove('hidden'); // Show Builder for students
    hrTab.classList.add('hidden'); // Hide HR for students
    switchView('student-view');
});

enterHR.addEventListener('click', () => {
    mainHeader.classList.remove('hidden');
    hrTab.classList.remove('hidden');
    studentTab.classList.add('hidden'); // Hide Student for HR
    resumeBuilderTab.classList.add('hidden'); // Hide Builder for HR
    switchView('hr-view');
});

logoutBtn.addEventListener('click', () => {
    mainHeader.classList.add('hidden');
    switchView('landing-view');
});

// Navigation
studentTab.addEventListener('click', () => switchView('student-view'));
resumeBuilderTab.addEventListener('click', () => switchView('resume-builder-view'));
hrTab.addEventListener('click', () => switchView('hr-view'));
backBtn.addEventListener('click', () => switchView('student-view'));

function switchView(viewId) {
    // Nav Tab Active State
    studentTab.classList.toggle('active', viewId === 'student-view');
    resumeBuilderTab.classList.toggle('active', viewId === 'resume-builder-view');
    hrTab.classList.toggle('active', viewId === 'hr-view');

    // View Visibility
    landingView.classList.remove('active');
    studentView.classList.remove('active');
    resumeBuilderView.classList.remove('active');
    hrView.classList.remove('active');
    resultsView.classList.remove('active');

    const target = document.getElementById(viewId);
    if (target) target.classList.add('active');

    lucide.createIcons();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// File Upload Logic - Student
dropzone.addEventListener('click', () => resumeInput.click());

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
});

resumeInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFile(e.target.files[0]);
});

function handleFile(file) {
    appState.file = file;
    fileNameDisplay.textContent = file.name;
    fileNameDisplay.style.color = '#6366f1';

    // Show role selection after file upload
    roleSelectionArea.classList.remove('hidden');
    roleSelectionArea.scrollIntoView({ behavior: 'smooth' });
}

// Role Selection Logic
roleOptions.forEach(chip => {
    chip.addEventListener('click', () => {
        // Toggle Active Class
        roleOptions.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');

        // Professional Role Descriptions for TF-IDF
        const role = chip.getAttribute('data-role');
        const roleData = {
            "IT Systems Administrator": "IT Systems Administrator experienced in managing IT infrastructure, servers, and networks. Skilled in system administration, troubleshooting, active directory, and server maintenance. Proficient in hardware configuration, technical support, and disaster recovery planning. Knowledge of security protocols and network performance optimization.",
            "Cloud Engineer": "Cloud Engineer specializing in AWS, Azure, and hybrid cloud migrations. Experience with cloud infrastructure optimization, server management, and cloud security. Proficient in Python, SQL, and automation. Skilled in architecting scalable and cost-effective cloud solutions.",
            "Cybersecurity Analyst": "Cybersecurity Analyst focused on risk management, security protocols, and incident reduction. Experienced in implementing cybersecurity measures, monitoring systems for threats, and conducting vulnerability assessments. Proficient in encryption, security operations (SOC), and information security best practices.",
            "Full Stack Developer": "Full stack web developer proficient in JavaScript, React, Node.js, Express, MongoDB, and SQL. Experience with HTML, CSS, Git, and REST APIs. Capable of building scalable web applications and managing both frontend and backend systems. Knowledge of TypeScript and Next.js is a plus.",
            "Data Scientist": "Data scientist with strong Python skills, including Machine Learning, Data Science libraries like Pandas, NumPy, and Scikit-learn. Proficiency in SQL and deep learning frameworks like TensorFlow or PyTorch. Analysis of large datasets and predictive modeling. Experience with data visualization tools like Tableau.",
            "Backend Developer": "Backend software engineer focused on Python, Java, and Node.js. Experience with Django, Flask, Express, and PostgreSQL. Proficiency in building REST APIs, managing Redis caching, database design, and server-side logic."
        };

        appState.jd = roleData[role] || "";
        jdInput.value = appState.jd;
    });
});

// Student Form Submit
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    appState.jd = jdInput.value.trim();
    const candidateName = nameInput.value.trim() || (appState.file ? appState.file.name.split('.')[0] : "Anonymous Candidate");

    if (!appState.file) {
        alert('Please upload a resume first.');
        return;
    }

    if (!appState.jd) {
        alert('Please select a role or provide a job description.');
        return;
    }

    analyzeApplication(candidateName);
});

// HR View Actions
hrDropzone.addEventListener('click', () => hrResumeInput.click());
hrDropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    hrDropzone.classList.add('dragover');
});

hrDropzone.addEventListener('dragleave', () => hrDropzone.classList.remove('dragover'));

hrDropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    hrDropzone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        appState.hrFiles = Array.from(e.dataTransfer.files);
        hrFileNameDisplay.textContent = `${appState.hrFiles.length} file(s) selected`;
        hrFileNameDisplay.style.color = '#6366f1';
    }
});

hrResumeInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        appState.hrFiles = Array.from(e.target.files);
        hrFileNameDisplay.textContent = `${appState.hrFiles.length} file(s) selected`;
        hrFileNameDisplay.style.color = '#6366f1';
    }
});

hrForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const jd = hrJdInput.value.trim();

    if (appState.hrFiles.length === 0 || !jd) {
        alert('Please provide Job Description and select at least one resume.');
        return;
    }

    processHRBulkUpload(jd);
});

// CORE API CALLS
async function analyzeApplication(name) {
    loader.classList.remove('hidden');

    const formData = new FormData();
    formData.append('resume', appState.file);
    formData.append('job_description', appState.jd);

    try {
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('API request failed');

        const data = await response.json();
        data.candidate_name = name;
        appState.results = data;

        displayResults(data);
        switchView('results-view');
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze. Please ensure the backend is running.');
    } finally {
        loader.classList.add('hidden');
    }
}

async function processHRBulkUpload(jd) {
    loader.classList.remove('hidden');

    const formData = new FormData();
    appState.hrFiles.forEach(file => formData.append('resumes', file));
    formData.append('job_description', jd);

    try {
        const response = await fetch('http://localhost:8000/hr/bulk-upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('API request failed');

        const data = await response.json();
        appState.hrResults = data.ranked_candidates;
        renderRanking();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process bulk upload. Please ensure the backend is running.');
    } finally {
        loader.classList.add('hidden');
    }
}

// RENDERING
function displayResults(data) {
    const isAuto = data.auto_analyzed;
    document.getElementById('res-candidate-name').textContent = data.candidate_name + (isAuto ? " (Auto-Fit Result)" : "");
    document.getElementById('score-text').textContent = data.score + '%';

    const statusBadge = document.getElementById('match-status');
    updateStatusBadge(statusBadge, data.score);

    renderChart(data.score);
    renderRadarChart(data.radar_data);

    // Insights
    const ins = data.market_insights || {};
    document.getElementById('res-salary').textContent = ins.estimated_salary || "$0k";
    document.getElementById('res-demand').textContent = ins.market_demand || "Normal";
    document.getElementById('res-remote').textContent = ins.remote_friendliness || "N/A";

    const foundContainer = document.getElementById('found-skills');
    const missingContainer = document.getElementById('missing-skills');
    const certsContainer = document.getElementById('found-certs');
    const expText = document.getElementById('res-experience');
    const senText = document.getElementById('res-seniority');

    foundContainer.innerHTML = '';
    missingContainer.innerHTML = '';
    certsContainer.innerHTML = '';

    // Features
    const f = data.features || {};
    expText.textContent = (f.experience_years || 0) + "+ Years";
    senText.textContent = f.seniority || "Junior";

    if (f.certifications && f.certifications.length > 0) {
        f.certifications.forEach(cert => {
            const pill = document.createElement('span');
            pill.className = 'pill found';
            pill.textContent = cert;
            certsContainer.appendChild(pill);
        });
    } else {
        certsContainer.innerHTML = '<span class="text-slate-500 text-xs">No specific certs detected</span>';
    }

    data.found_skills.forEach(skill => {
        const span = document.createElement('span');
        span.className = 'pill found';
        span.textContent = skill;
        foundContainer.appendChild(span);
    });

    if (data.missing_skills.length > 0) {
        data.missing_skills.forEach(skill => {
            const span = document.createElement('span');
            span.className = 'pill missing';
            span.textContent = skill;
            missingContainer.appendChild(span);
        });
    } else {
        missingContainer.innerHTML = '<span class="text-slate-400 italic text-sm">Target fully matched!</span>';
    }

    // Trajectory
    renderTrajectory(data.career_trajectories);

    // Skill Simulator
    simulatorSection.style.display = 'block';
    simResult.classList.add('hidden');
    simSkillsInput.value = '';

    lucide.createIcons();
}

function renderTrajectory(trajectories) {
    if (trajectories && trajectories.length > 0) {
        trajectorySection.style.display = 'block';
        trajectoryContainer.innerHTML = '';
        trajectories.forEach(traj => {
            const tCard = document.createElement('div');
            tCard.className = 'card glass fit-card';
            let timelineHtml = traj.progression.map((p, i) => `
                <div style="margin-top: 1rem; position: relative; padding-left: 1.5rem; border-left: 2px solid #6366f1;">
                    <div style="position: absolute; left: -6px; top: 0; width: 10px; height: 10px; border-radius: 50%; background: #6366f1;"></div>
                    <strong style="color: #fff; font-size: 0.9rem;">${p.stage}</strong>
                    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Specializing in: ${p.focus}</p>
                </div>
            `).join('');

            tCard.innerHTML = `
                <h4 style="color: #a855f7">${traj.possible_career}</h4>
                <div class="mt-4">${timelineHtml}</div>
                <div class="mt-6" style="font-size: 0.8rem;">
                    <strong style="color: #10b981;">Required Skill Additions:</strong>
                    <p style="color: #94a3b8;">${traj.recommended_additions.join(', ')}</p>
                </div>
            `;
            trajectoryContainer.appendChild(tCard);
        });
    } else {
        trajectorySection.style.display = 'none';
    }
}

// Simulator Trigger
simBtn.addEventListener('click', async () => {
    const potSkillsStr = simSkillsInput.value.trim();
    const potSkills = potSkillsStr.split(',').map(s => s.trim()).filter(s => s);

    if (!potSkills.length || !appState.results) return;

    simBtn.textContent = "Simulating Evolution...";
    simBtn.disabled = true;

    try {
        const response = await fetch('http://localhost:8000/student/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                resume_text: appState.results.resume_text,
                jd_text: appState.results.jd_text,
                potential_skills: potSkills
            })
        });

        if (response.ok) {
            const data = await response.json();
            simResult.classList.remove('hidden');
            simResult.innerHTML = `
                <div style="margin-bottom: 0.5rem;"><strong>Starting Mark:</strong> ${Math.round(data.current_score)}%</div>
                <div><strong>Predicted Future Score:</strong> <span style="font-size: 1.5rem; color: #10b981; font-weight: 800;">${Math.round(data.future_score)}%</span></div>
                <small style="color: #94a3b8;">Significant growth of +${Math.round(data.improvement)}% projected!</small>
            `;
        } else {
            const errData = await response.text();
            console.error('Simulation Failed:', errData);
            alert('Simulation failed. Check console for details.');
        }
    } catch (e) {
        console.error('Simulation Error:', e);
        alert('A network error occurred during simulation.');
    } finally {
        simBtn.textContent = "Simulate Growth";
        simBtn.disabled = false;
    }
});

function renderRanking() {
    rankingBody.innerHTML = '';
    if (appState.hrResults.length === 0) {
        rankingBody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 4rem; color: #64748b;">No matching candidates processed yet.</td></tr>';
        return;
    }

    appState.hrResults.forEach((item, index) => {
        const tr = document.createElement('tr');
        const topSkills = item.found_skills.slice(0, 4).map(s =>
            `<span class="pill found" style="font-size: 0.7rem; padding: 2px 8px; margin: 2px;">${s}</span>`
        ).join('') + (item.found_skills.length > 4 ? '<span style="color: #64748b; font-size: 0.7rem; margin-left: 4px;">...</span>' : '');

        tr.innerHTML = `
    <td><span class="rank-num">#${item.rank}</span></td>
    <td><div style="font-weight: 600; color: #fff;">${item.candidate_name}</div></td>
    <td><div style="font-weight: 700; color: #6366f1;">${item.overall_match}%</div></td>
    <td><div style="font-weight: 500; color: #10b981;">${item.skill_match}%</div></td>
    <td style="display: flex; flex-wrap: wrap; gap: 4px; padding: 12px 8px;">${topSkills || '<span style="color: #64748b; font-style: italic; font-size: 0.8rem;">No JD Overlap</span>'}</td>
`;
        rankingBody.appendChild(tr);
    });
}

// Export CSV
exportBtn.addEventListener('click', () => {
    if (!appState.hrResults.length) return;
    let csv = "Rank,Candidate,Match Score,Skill Overlap\n";
    appState.hrResults.forEach((row, i) => {
        csv += `${i + 1},"${row.candidate_name}",${row.overall_match}%,${row.skill_match}%\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.setAttribute("href", url);
    a.setAttribute("download", "talent_match_shortlist.csv");
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
});

function updateStatusBadge(badge, score) {
    if (score > 80) {
        badge.textContent = 'Elite Candidate Match';
        badge.style.color = '#10b981';
        badge.style.background = 'rgba(16, 185, 129, 0.1)';
    } else if (score > 60) {
        badge.textContent = 'High Potential Hire';
        badge.style.color = '#6366f1';
        badge.style.background = 'rgba(99, 102, 241, 0.1)';
    } else if (score > 40) {
        badge.textContent = 'Good Foundational Skills';
        badge.style.color = '#f59e0b';
        badge.style.background = 'rgba(245, 158, 11, 0.1)';
    } else {
        badge.textContent = 'Development Needed';
        badge.style.color = '#ef4444';
        badge.style.background = 'rgba(239, 68, 68, 0.1)';
    }
}

function renderChart(score) {
    const ctx = document.getElementById('scoreChart').getContext('2d');
    if (scoreChart) scoreChart.destroy();
    scoreChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: ['#6366f1', 'rgba(255,255,255,0.05)'],
                borderWidth: 0,
                borderRadius: 20
            }]
        },
        options: {
            cutout: '85%',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { tooltip: { enabled: false } }
        }
    });
}

function renderRadarChart(data) {
    const ctx = document.getElementById('radarChart').getContext('2d');
    if (radarChart) radarChart.destroy();

    radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Your Resume',
                    data: data.resume_values,
                    backgroundColor: 'rgba(99, 102, 241, 0.2)',
                    borderColor: '#6366f1',
                    pointBackgroundColor: '#6366f1',
                    borderWidth: 2
                },
                {
                    label: 'Job Goal',
                    data: data.jd_values,
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: '#10b981',
                    pointBackgroundColor: '#10b981',
                    borderWidth: 2
                }
            ]
        },
        options: {
            scales: {
                r: {
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { color: '#94a3b8', font: { size: 10 } },
                    ticks: { display: false, stepSize: 2 },
                    suggestedMin: 0,
                    suggestedMax: 10
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', boxWidth: 10, font: { size: 10 } }
                }
            },
            maintainAspectRatio: false
        }
    });
}

// Resume Builder Elements
const rbName = document.getElementById('rb-name');
const rbTitle = document.getElementById('rb-title');
const rbContact = document.getElementById('rb-contact');
const rbSummary = document.getElementById('rb-summary');
const rbSkills = document.getElementById('rb-skills');
const rbExpContainer = document.getElementById('rb-exp-container');
const addExpBtn = document.getElementById('add-exp-btn');
const downloadResumeBtn = document.getElementById('download-resume-btn');

// Preview Elements
const pvName = document.getElementById('pv-name');
const pvTitle = document.getElementById('pv-title');
const pvContact = document.getElementById('pv-contact');
const pvSummary = document.getElementById('pv-summary');
const pvExperience = document.getElementById('pv-experience');
const pvSkills = document.getElementById('pv-skills');

// Resume Builder Logic
const updateResumePreview = () => {
    if (!pvName) return;
    pvName.textContent = rbName.value || 'Candidate Name';
    pvTitle.textContent = rbTitle.value || 'Professional Title';
    pvContact.textContent = rbContact.value || 'john@email.com | +123 | Location';
    pvSummary.textContent = rbSummary.value || 'Write a brief overview of your career...';

    // Update Skills
    pvSkills.innerHTML = '';
    const skills = rbSkills.value.split(',').map(s => s.trim()).filter(s => s);
    skills.forEach(skill => {
        const span = document.createElement('span');
        span.className = 'pill';
        span.textContent = skill;
        pvSkills.appendChild(span);
    });

    // Update Experience
    pvExperience.innerHTML = '';
    const entries = rbExpContainer.querySelectorAll('.exp-entry');
    entries.forEach(entry => {
        const company = entry.querySelector('.rb-exp-company').value;
        const role = entry.querySelector('.rb-exp-role').value;
        const desc = entry.querySelector('.rb-exp-desc').value;

        if (company || role) {
            const item = document.createElement('div');
            item.className = 'pv-exp-item';

            const descHtml = desc.split('\n').filter(l => l.trim()).map(l => `<li>${l}</li>`).join('');

            item.innerHTML = `
                <div class="pv-exp-header">
                    <span>${role || 'Role'}</span>
                    <span style="color: #6b7280;">${company || 'Company'}</span>
                </div>
                <ul class="pv-exp-desc">${descHtml}</ul>
            `;
            pvExperience.appendChild(item);
        }
    });
};

// Event Listeners for Builder
if (rbName) {
    [rbName, rbTitle, rbContact, rbSummary, rbSkills].forEach(el => {
        el.addEventListener('input', updateResumePreview);
    });

    addExpBtn.addEventListener('click', () => {
        const div = document.createElement('div');
        div.className = 'exp-entry glass p-4 mb-4';
        div.style.padding = '1rem';
        div.style.borderRadius = '0.5rem';
        div.innerHTML = `
            <input type="text" class="input-field mb-2 rb-exp-company" placeholder="Company Name">
            <input type="text" class="input-field mb-2 rb-exp-role" placeholder="Role">
            <textarea class="input-field rb-exp-desc" placeholder="Responsibilities (one per line)"></textarea>
            <button class="btn-text" style="color: #ef4444; font-size: 0.8rem; margin-top: 0.5rem;" onclick="this.parentElement.remove(); updateResumePreview();">Remove</button>
        `;
        rbExpContainer.appendChild(div);

        div.querySelectorAll('input, textarea').forEach(input => {
            input.addEventListener('input', updateResumePreview);
        });
    });

    // Initial Exp Listeners
    rbExpContainer.querySelectorAll('input, textarea').forEach(input => {
        input.addEventListener('input', updateResumePreview);
    });

    // Export Logic
    downloadResumeBtn.addEventListener('click', () => {
        const element = document.getElementById('resume-preview-doc');
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head>
                    <title>Resume - ${rbName.value}</title>
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                        body { margin: 0; padding: 0; background: white; }
                        .resume-sheet { padding: 40px; font-family: 'Inter', sans-serif; color: #1a1a1a; line-height: 1.5; }
                        .header-section { border-bottom: 2px solid #6366f1; padding-bottom: 20px; margin-bottom: 20px; }
                        h1 { font-size: 28pt; margin: 0; color: #111827; }
                        h3 { font-size: 14pt; color: #4f46e5; margin: 5px 0; text-transform: uppercase; }
                        .contact-line { font-size: 10pt; color: #6b7280; }
                        .section { margin-bottom: 20px; text-align: left; }
                        .section-title { font-size: 10pt; font-weight: 700; color: #111827; text-transform: uppercase; border-bottom: 1px solid #e5e7eb; margin-bottom: 10px; padding-bottom: 5px; }
                        p, li { font-size: 10pt; color: #374151; }
                        .pv-exp-header { display: flex; justify-content: space-between; font-weight: 600; margin-bottom: 5px; color: #111827; }
                        .pv-exp-desc { padding-left: 20px; margin: 5px 0; list-style: disc; }
                        .skill-pills-row { display: flex; flex-wrap: wrap; gap: 5px; }
                        .pill { background: #f3f4f6; color: #374151; padding: 3px 10px; border-radius: 4px; border: 1px solid #d1d5db; font-size: 9pt; }
                    </style>
                </head>
                <body>
                    <div class="resume-sheet">
                        ${element.innerHTML}
                    </div>
                    <script>setTimeout(() => { window.print(); window.close(); }, 500);</script>
                </body>
            </html>
        `);
        printWindow.document.close();
    });
}
