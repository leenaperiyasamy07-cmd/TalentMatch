ROADMAP_DATA = {
    "sql": [
        "Learn database basics & ER diagrams",
        "Practice SELECT queries (Filtering, Sorting, Aliases)",
        "Master JOIN operations & Aggregate functions",
        "Explore Indexing and Query Optimization",
        "Build a mini project using PostgreSQL or MySQL"
    ],
    "python": [
        "Setup environment & basic syntax (Loops, Conditionals)",
        "Master Collections (Lists, Dicts, Sets, Tuples)",
        "Learn functional programming (Lambda, Map, Filter)",
        "Understand OOP concepts in Python",
        "Build a project using Flask or FastAPI"
    ],
    "machine learning": [
        "Learn Data Preprocessing (NumPy, Pandas)",
        "Study Supervised Learning (Regression, Classification)",
        "Understand Unsupervised Learning (Clustering, PCA)",
        "Practice using Scikit-learn on Kaggle datasets",
        "Build a prediction model project"
    ],
    "react": [
        "Master Modern JS (ES6+, Promises, Async/Await)",
        "Learn Core React Concepts (JSX, Cleanup, Virtual DOM)",
        "State Management (useState, useEffect, Context API)",
        "Learn Routing with React Router",
        "Build a complete CRUD application"
    ],
    "javascript": [
        "Basics: Variables, Scope, and Closures",
        "Asynchronous JS: Callbacks, Promises, Async/Await",
        "DOM Manipulation and Event Listeners",
        "Fetch API and Integration with Backend",
        "Build an interactive web tool"
    ],
    "docker": [
        "Understand Containers vs Virtual Machines",
        "Learn Dockerfile syntax and base images",
        "Manage images, containers, and volumes",
        "Learn Docker Compose for multi-container apps",
        "Containerize a full-stack application"
    ],
    "git": [
        "Basics: Init, Add, Commit, and Status",
        "Branching: Checkout, Merge, and Rebase",
        "Remote: Clone, Push, Pull, and Fetch",
        "Handling Merge Conflicts & Using Stash",
        "Collaborate on a project using Pull Requests"
    ],
    "java": [
        "Learn Java Syntax & JVM Architecture",
        "Master OOP: Inheritance, Polymorphism, Abstraction",
        "Java Collections Framework (List, Map, Set)",
        "Exception Handling and Multithreading",
        "Build a backend API using Spring Boot"
    ],
    "ai": [
        "Learn Mathematics for AI (Linear Algebra, Calculus)",
        "Master Python & Data Libraries (NumPy, Pandas)",
        "Study Machine Learning Fundamentals",
        "Explore Neural Networks & Deep Learning",
        "Deploy an AI Model using Flask or FastAPI"
    ],
    "artificial intelligence": [
        "Introduction to AI & Search Algorithms",
        "Knowledge Representation and Logic",
        "Machine Learning & Statistical Modeling",
        "Neural Networks and Deep Learning",
        "Ethical AI and Future Trends"
    ]
}

def generate_roadmap(missing_skills):
    roadmap = {}
    for skill in missing_skills:
        skill_lower = skill.lower()
        if skill_lower in ROADMAP_DATA:
            roadmap[skill] = ROADMAP_DATA[skill_lower]
        else:
            # Generic steps for unknown skills
            roadmap[skill] = [
                f"Understand the core concepts of {skill}",
                f"Search for top-rated courses on Coursera/Udemy for {skill}",
                f"Build a basic Hello World or tutorial project",
                f"Explore advanced features and best practices",
                f"Contribute to an open-source project or build a portfolio item"
            ]
    return roadmap
