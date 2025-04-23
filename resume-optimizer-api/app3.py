from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from huggingface_hub import InferenceClient

app = Flask(__name__)
CORS(app)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define your skill list and skill graph
skills_list = [
    "Java", "Spring Boot", "JSF", "JSP",
    "JavaScript", "React.js", "Redux", "Node.js",
    "Python", "Flask", "Django"
]

skill_graph = {
    "Java": ["Spring Boot", "JSF", "JSP"],
    "JavaScript": ["React.js", "Redux", "Node.js"],
    "React.js": ["Redux"],
    "Python": ["Flask", "Django"]
}

# Load Hugging Face inference client for resume generation
client = InferenceClient(token="")

# Extract skills based on keyword matching
def extract_skills(text, skill_list):
    return [skill for skill in skill_list if skill.lower() in text.lower()]

# Suggest missing skills using the graph and job context
def suggest_from_graph(resume_skills, job_skills, skill_graph):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    # 1. Skills in job description but not in resume
    missing_from_job = job_set - resume_set

    # 2. Filter related skills only if they also exist in job description
    related_skills = set()
    for skill in resume_set:
        related = skill_graph.get(skill, [])
        related_skills.update([r for r in related if r in job_set])

    # Final suggestions: only skills from job description
    suggestions = (missing_from_job & related_skills) - resume_set
    return list(suggestions)

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
    suggested_skills = suggest_from_graph(resume_skills, job_skills, skill_graph)

    return jsonify({
        "resume_skills": resume_skills,
        "job_skills": job_skills,
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
