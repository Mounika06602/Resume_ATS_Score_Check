# ResumeMatch AI — Premium ATS Analyzer & Score Simulator

ResumeMatch AI is a modern, AI-powered web application that analyzes how well a resume aligns with a given Job Description (JD). Utilizing Google's Gemini models via LangChain, it simulates Applicant Tracking System (ATS) parsing to calculate a match score, identify matching/missing keywords, and generate actionable structural and content suggestions to improve the resume.

---

## 🌟 Key Features

* **Docx & PDF Extraction**: In-memory text extraction for PDF, DOCX, and TXT resume files.
* **ATS Score Simulation**: Calculates a match score out of 100% and displays a simulated breakdown across factors like Keyword Relevance, Experience Alignment, and Formatting.
* **Semantic Keyword Auditing**: Extracts key matching skills (found in both documents) and alerts you to missing/weak skills mentioned in the job description.
* **Actionable Improvement Checklist**: Generates specific suggestions to optimize experience phrasing, layout, and keyword inclusion.
* **Premium User Interface**: Modern dark-themed dashboard with glassmorphism styling, clean SVG progress arcs, dynamic loading states, and full layout responsiveness.
* **Secure Server-Side Configuration**: Keep your Gemini API key safe in a local server-side configuration file (`.env`) rather than exposing it in the client UI.

---

## 🛠️ Technology Stack

* **Frontend**: HTML5 (Semantic Structure), Custom Vanilla CSS3 (Glassmorphic Design, Animations), Vanilla JavaScript (File Handling, Dynamic SVG animations).
* **Backend**: Python 3.12, FastAPI (Async Web Framework), Uvicorn.
* **AI/LLM Orchestration**: LangChain, `langchain-google-genai` (integration with Gemini 2.5/2.0 Flash models).
* **Document Parsing**: `pypdf`, `python-docx`.

---

## 📂 Project Structure

```
resume-ats-score-check/
├── static/
│   ├── index.html        # Main dashboard UI
│   ├── style.css         # Custom premium dark styling
│   └── main.js           # File dropzone and api rendering logic
├── .env                  # Server-side API key configuration (git-ignored)
├── .gitignore            # Git rules to prevent uploading keys/caches
├── app/                  # Application modular package
│   ├── main.py           # FastAPI config, static serving, and entry runner
│   ├── analyzer.py       # Document parsing & Gemini LangChain logic
│   └── api/
│       └── routes.py     # API HTTP routes
├── requirements.txt      # Python dependencies list
└── README.md             # Project documentation (this file)
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have **Python 3.12+** installed on your system.

### 2. Clone and Setup
Open your terminal inside the project directory and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key
Create a `.env` file in the root directory (a template is provided) and paste your Google Gemini API Key:
```env
GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
PORT=8000
```
*(You can get a free API key from [Google AI Studio](https://aistudio.google.com/))*

### 4. Run the Server
Launch the backend FastAPI application:
```bash
python app/main.py
```
The server will start on **`http://127.0.0.1:8000`**.

---

## 🧪 Verification & Usage

1. Open **`http://127.0.0.1:8000`** in your browser.
2. Drag and drop any PDF, DOCX, or TXT resume file into the document upload zone.
3. Paste the target job description requirements into the Job Description box.
4. Click **Analyze Fit** to run the ATS score simulation and receive recommendations.
