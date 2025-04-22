# import requests
# import spacy
# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
#
# # Hugging Face API Key (Replace with your own)
# HUGGINGFACE_API_KEY = ""
#
# # Hugging Face Model URL
# API_URL = "https://api-inference.huggingface.co/models/linkedin/relevance"
#
# # Headers for API request
# HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
#
#
# def check_relevance(resume_text, job_description_text):
#     """Compare resume and job description relevance using LinkedIn model."""
#     payload = {
#         "inputs": {
#             "text1": resume_text,
#             "text2": job_description_text
#         }
#     }
#     response = requests.post(API_URL, headers=HEADERS, json=payload)
#
#     if response.status_code == 200:
#         return response.json()  # Returns a relevance score
#     else:
#         return {"error": response.json()}  # Error handling
#
#
# @app.route('/check_relevance', methods=['POST'])
# def check_relevance_endpoint():
#     """API endpoint to check resume vs. job description relevance."""
#     data = request.json
#     resume_text = data.get("resume_text", "")
#     job_description_text = data.get("job_description_text", "")
#
#     relevance_score = check_relevance(resume_text, job_description_text)
#
#     return jsonify({
#         "relevance_score": relevance_score
#     })
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
import spacy
from flask import Flask, request, jsonify
from flask_cors import CORS
from joblib import load

app = Flask(__name__)
CORS(app)

# Load a spaCy model for fallback or keyword matching
nlp = spacy.load("en_core_web_sm")
print("spaCy model loaded.")

# Load trained classifier and label binarizer
clf = load("skill_classifier.joblib")
mlb = load("skill_mlb.joblib")
print("Classifier and label binarizer loaded.")

# Define a list of known skills (must match training set)
skills_list = list(mlb.classes_)
print(f"Known skills list loaded with {len(skills_list)} skills.")

# Extract skills using simple keyword match
def extract_skills(text, skills_list):
    matched_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    print(f"Extracted skills from text: {matched_skills}")
    return matched_skills

# Suggest missing skills using the trained model
def suggest_missing_skills(resume_skills, job_skills):
    known_skills = list(set(resume_skills) | set(job_skills))
    print(f"Known skills (resume + job): {known_skills}")
    input_vector = mlb.transform([known_skills])
    prediction_vector = clf.predict(input_vector)
    predicted_skills = mlb.inverse_transform(prediction_vector)[0]
    suggestions = list(set(predicted_skills) - set(known_skills))
    print(f"Suggested missing skills: {suggestions}")
    return suggestions

@app.route('/extract_skills', methods=['POST'])
def extract_skills_api():
    data = request.json
    resume_text = data.get('resume_text', '')
    job_description_text = data.get('job_description_text', '')

    print("\n--- New Request ---")
    print(f"Resume Text: {resume_text}")
    print(f"Job Description Text: {job_description_text}")

    # Extract skills from text
    resume_skills = extract_skills(resume_text, skills_list)
    job_skills = extract_skills(job_description_text, skills_list)

    # Suggest missing skills using ML model
    suggested_skills = suggest_missing_skills(resume_skills, job_skills)

    return jsonify({
        'resume_skills': resume_skills,
        'job_skills': job_skills,
        'suggested_skills': suggested_skills
    })

if __name__ == '__main__':
    app.run(debug=True)
