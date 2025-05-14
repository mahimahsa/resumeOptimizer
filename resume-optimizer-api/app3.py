from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from huggingface_hub import InferenceClient

app = Flask(__name__)
CORS(app)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define an expanded list of skills
skills_list = [
    # Languages
    "Python", "JavaScript", "Java", "C#", "C++", "Go", "Ruby", "PHP", "TypeScript", "SQL", "HTML", "CSS",

    # Frontend Frameworks
    "React.js", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js",

    # Backend Frameworks
    "Node.js", "Express.js", "Spring Boot", "Django", "Flask", "ASP.NET", "Ruby on Rails", "Laravel",

    # Databases
    "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Oracle", "Firebase",

    # DevOps & Tools
    "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "CI/CD", "Jenkins", "Terraform", "AWS", "Azure", "GCP",

    # Testing
    "Jest", "Mocha", "Chai", "JUnit", "Selenium", "Cypress",

    # Architecture & Methodologies
    "REST", "GraphQL", "Microservices", "Monolith", "MVC", "Agile", "Scrum", "Kanban", "TDD", "DDD", "Microfrontend",

    # Soft Skills & Collaboration
    "Teamwork", "Communication", "Problem Solving", "Leadership", "Time Management",

    # Programming Roles
    "Frontend Developer", "Backend Developer", "Full Stack Developer", "DevOps Engineer", "QA Engineer",
    "Software Architect", "Tech Lead", "Mobile Developer", "Data Engineer", "ML Engineer", "AI Researcher"
]

# Define a more complete skill graph with all skills mapped
skill_graph = {
    # Languages and ecosystems
    "JavaScript": ["React.js", "Vue.js", "Angular", "Node.js", "Next.js", "TypeScript"],
    "Python": ["Django", "Flask", "Pandas", "NumPy", "FastAPI"],
    "Java": ["Spring Boot", "JUnit"],
    "C#": ["ASP.NET"],
    "Ruby": ["Ruby on Rails"],
    "PHP": ["Laravel"],

    # Frameworks and their tools
    "React.js": ["Redux", "Next.js", "Jest", "TypeScript"],
    "Vue.js": ["Vuex", "Nuxt.js"],
    "Node.js": ["Express.js", "Mocha"],
    "Django": ["REST", "PostgreSQL"],
    "Flask": ["REST"],
    "Svelte": ["TypeScript"],

    # Databases
    "MongoDB": ["Mongoose"],
    "PostgreSQL": ["SQLAlchemy"],
    "MySQL": [],
    "SQLite": [],
    "Redis": [],
    "Oracle": [],
    "Firebase": [],

    # DevOps
    "Docker": ["Kubernetes"],
    "Git": ["GitHub", "GitLab"],
    "CI/CD": ["Jenkins", "GitHub Actions"],

    # Cloud
    "AWS": ["Lambda", "S3", "EC2"],
    "Azure": ["Functions", "App Service"],
    "GCP": ["Cloud Run", "Firestore"],

    # Methodologies
    "Agile": ["Scrum", "Kanban"],
    "TDD": ["JUnit", "Jest"],
    "DDD": ["Software Architect", "Backend Developer"],
    "MVC": ["Software Architect", "Frontend Developer"],
    "Monolith": ["Software Architect", "Backend Developer"],

    # Testing
    "Jest": ["React.js", "TDD"],
    "Mocha": ["Node.js", "TDD"],
    "Chai": ["Mocha"],
    "JUnit": ["Java", "TDD"],
    "Selenium": ["QA Engineer"],
    "Cypress": ["QA Engineer"],

    # Soft Skills
    "Teamwork": ["Communication", "Problem Solving"],
    "Leadership": ["Time Management", "Problem Solving"],

    # Roles
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React.js", "Vue.js", "REST", "GraphQL", "Microfrontend", "Cloud", "Soft Skills"],
    "Backend Developer": ["Node.js", "Java", "Spring Boot", "Flask", "Cloud", "Soft Skills"],
    "Full Stack Developer": ["React.js", "Node.js", "MongoDB", "PostgreSQL", "Cloud", "Soft Skills"],
    "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "AWS", "Azure", "Cloud", "Soft Skills"],
    "QA Engineer": ["Selenium", "Cypress", "Mocha", "Soft Skills"],
    "Mobile Developer": ["React Native", "Flutter", "Soft Skills"],
    "Data Engineer": ["SQL", "Python", "ETL", "Airflow", "Soft Skills"],
    "ML Engineer": ["Python", "TensorFlow", "PyTorch", "Soft Skills"],
    "AI Researcher": ["Python", "NLP", "Deep Learning", "Soft Skills"],

    # Aggregates
    "Cloud": ["AWS", "Azure", "GCP"],
    "Soft Skills": ["Teamwork", "Communication", "Problem Solving", "Leadership", "Time Management"]
}

# Build reverse graph
reverse_graph = {}
for parent, children in skill_graph.items():
    for child in children:
        reverse_graph.setdefault(child, []).append(parent)

# Suggest only if one of the direct parents is in resume_skills
def filter_suggested_skills(missing_skills, resume_skills):
    suggestions = []
    for skill in missing_skills:
        parents = reverse_graph.get(skill, [])
        if any(p in resume_skills for p in parents):
            suggestions.append(skill)
    return suggestions

# Reverse graph: child → [parents]
reverse_graph = {}
for parent, children in skill_graph.items():
    for child in children:
        reverse_graph.setdefault(child, []).append(parent)

# Extract skills based on keyword matching
def extract_skills(text, skill_list):
    return [skill for skill in skill_list if skill.lower() in text.lower()]

# Suggest missing skills using reverse_graph and direct parent lookup
def filter_suggested_skills(missing_skills, resume_skills):
    suggestions = []
    for skill in missing_skills:
        parents = reverse_graph.get(skill, [])
        if any(p in resume_skills for p in parents):
            suggestions.append(skill)
    return suggestions

@app.route('/extract_skills', methods=['POST'])
def extract_skills_api():
    data = request.json
    resume_text = data.get('resume_text', '')
    job_description_text = data.get('job_description_text', '')

    print("\n--- New Request ---")
    print(f"Resume: {resume_text}")
    print(f"Job Desc: {job_description_text}")

    resume_skills = extract_skills(resume_text, skills_list)
    job_skills = extract_skills(job_description_text, skills_list)

    missing_skills = list(set(job_skills) - set(resume_skills))
    suggested_skills = filter_suggested_skills(missing_skills, resume_skills)

    return jsonify({
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "missing_skills": missing_skills,
        "suggested_skills": suggested_skills
    })

@app.route('/finalize_skills', methods=['POST'])
def finalize_skills():
    data = request.json
    resume_skills = data.get('resume_skills', [])
    selected_skills = data.get('selected_skills', [])
    resume_text = data.get("resume_text", "")

    final_skills = list(set(resume_skills + selected_skills))
    skill_str = ", ".join(selected_skills)

    prompt = f"""
You are a resume improvement assistant.

Your job is to enhance the following resume by integrating only the skills listed below.

Allowed skills to add: {skill_str}

Important:
- Do NOT remove or replace any existing content.
- Keep the original tone and sentence structure.
- Insert the new skills in appropriate places where they fit logically.
- Write full sentences — not a skill list.
- Do NOT generate a new resume from scratch.

Original resume:
\"\"\"{resume_text}\"\"\"

Improved resume:
"""
    #todo: paste your HuggingFace key here as token
    client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token="")  # Make sure to set your token
    response = client.text_generation(prompt, max_new_tokens=300)
    improved_resume = response.strip()

    print("\n--- Regenerated Resume ---\n")
    print(improved_resume)

    return jsonify({
        "final_skills": final_skills,
        "regenerated_resume": improved_resume
    })

if __name__ == '__main__':
    app.run(debug=True)