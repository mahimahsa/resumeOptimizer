# 🧠 Resume Optimizer

A full-stack AI-powered resume optimizer that enhances resumes based on job descriptions using skill extraction and generative AI.

Built with:
- 🔥 Flask (Python) — for backend API and AI integration
- ⚛️ Next.js (TypeScript) — for frontend interface and state management
- 🤖 Hugging Face Inference API — for LLM-based resume generation

---

## ✨ Features

- Extracts skills from user resume and job description
- Suggests missing skills using a predefined skill graph
- Lets users choose skills to add
- Regenerates resume using AI (LLM)
- Allows copying the improved resume to clipboard

---

## 📁 Folder Structure

```
resumeOptimizer/
├── resume_optimizer_api/   # Flask backend
│   └── app.py              # Core backend logic
├── resume_optimizer_ui/    # Next.js frontend
│   ├── components/         # React components
│   ├── pages/              # Main pages (resume UI)
│   └── store/              # Redux state management
└── README.md               # Project documentation
```

---

## 🚀 Setup Instructions

### 🔧 Backend (Flask API)

```bash
cd resume_optimizer_api
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
```

Edit `app.py` to include your Hugging Face token:

```python
client = InferenceClient(token="your_huggingface_token")
```

Start the API:
```bash
python app.py
```

Runs at: `http://localhost:5000`

---

### 💻 Frontend (Next.js)

```bash
cd resume_optimizer_ui
npm install
npm run dev
```

Open in browser: `http://localhost:3000`

---

## 📦 API Endpoints

| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| POST   | `/extract_skills`  | Extract resume and job description skills |
| POST   | `/finalize_skills` | Suggest and regenerate updated resume |

---

## 🛠️ Roadmap

- [ ] Export regenerated resume to PDF
- [ ] Add login and user accounts
- [ ] Store and compare resume versions
- [ ] Deploy full stack (Render, Railway, Vercel)

---

## 📄 License & Credits

- MIT License — open for personal and commercial use
- Powered by:
  - [Hugging Face](https://huggingface.co) for AI inference
  - [Next.js](https://nextjs.org) and [Redux Toolkit](https://redux-toolkit.js.org)
