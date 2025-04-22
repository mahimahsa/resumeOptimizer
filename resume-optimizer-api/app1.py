import spacy
from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient

app = Flask(__name__)
CORS(app)

# Load a spaCy model
nlp = spacy.load("en_core_web_sm")

# Define a list of known skills
skills_list = ["Python", "JavaScript", "Machine Learning", "data analysis",
               "software engineering", "Flask", "SQL", "Java", "C#", "Spring Boot", "JSF", "JSP", "React.js", "Redux"]

# Define a basic internal skill graph
skill_graph = {
    "Java": ["Spring Boot", "JSF", "JSP"],
    "JavaScript": ["React.js", "Redux", "Node.js"],
    "Python": ["Flask", "Django", "Pandas"],
    "React.js": ["Redux"]
}

# Initialize Hugging Face Inference Client
hf_token = null  # replace with your actual key
client = InferenceClient(token=hf_token)

# Extract known skills using simple keyword match
def extract_skills(text, skills_list):
    skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return skills

# Prompt LLM to suggest missing skills based on graph and context
def suggest_missing_skills(resume_skills, job_skills):
    resume_str = ", ".join(resume_skills)
    job_str = ", ".join(job_skills)

    graph_prompt = "Here is a skill graph for reference:\n"
    for category, items in skill_graph.items():
        graph_prompt += f"- {category}: {items}\n"

    prompt = f"""
You are a smart assistant that helps users improve their resumes.

{graph_prompt}

Resume skills: {resume_str}
Job description skills: {job_str}

Suggest relevant but missing skills that are:
1. Present in the job description and not in the resume, OR
2. Strongly related to the resume skills based on the graph.

Only return a list of suggested skills. No explanation.
"""

    response = client.text_generation(prompt, max_new_tokens=100)
    return response.strip()

@app.route('/extract_skills', methods=['POST'])
def extract_skills_api():
    data = request.json
    resume_text = data.get('resume_text', '')
    job_description_text = data.get('job_description_text', '')

    # Extract explicit skills
    resume_skills = extract_skills(resume_text, skills_list)
    job_skills = extract_skills(job_description_text, skills_list)

    # Suggest missing skills using LLM and internal skill graph
    suggestions = suggest_missing_skills(resume_skills, job_skills)

    return jsonify({
        'resume_skills': resume_skills,
        'job_skills': job_skills,
        'suggested_skills': suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)
