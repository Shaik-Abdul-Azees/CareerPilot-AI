# CareerPilot AI — AI-Powered Job Application Assistant

🌐 **Live Demo:** [Launch CareerPilot AI](https://careerpilot-ai-cqtaoaw9vdazgkpqtt73ds.streamlit.app/)

💻 **GitHub Repository:** [CareerPilot-AI](https://github.com/Shaik-Abdul-Azees/CareerPilot-AI)

---


CareerPilot AI is a Python-based application that helps job seekers analyze resumes, estimate ATS compatibility, compare their skills against job descriptions, receive AI-generated career recommendations, and track job applications.

## Features

- **Resume Analysis:** Extracts and analyzes text from PDF resumes.
- **ATS Compatibility Estimate:** Evaluates resume completeness, section headings, contact details, and other indicators to provide an estimated score.
- **Job Description Matching:** Identifies matching and missing skills from a resume and job description.
- **AI Career Recommendations:** Uses a locally hosted language model through Ollama to generate personalized recommendations.
- **Application Tracker:** Stores and manages job application details using SQLite.
- **Interactive UI:** Provides an interface built with Streamlit.

## Technology Stack

- Python
- Streamlit
- Ollama and Qwen2.5
- PyMuPDF
- SQLite
- Pytest

## Project Structure

```text
AI Job Application Agent/
├── app.py
├── src/
│   ├── ai/
│   ├── analysis/
│   ├── api/
│   ├── database/
│   ├── matching/
│   └── parser/
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Prerequisites

- Python 3.10 or a compatible version
- pip
- Ollama installed locally
- The Qwen2.5 3B model available in Ollama

## Setup

1. Clone or download this repository.
2. Create and activate a virtual environment.
3. Install the project dependencies.
4. Ensure Ollama is running and the required model is available.
5. Start the application.

Example commands for Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull qwen2.5:3b
streamlit run app.py
```

## Running Tests

Run the automated tests with:

```powershell
python -m pytest -v
```

## Privacy and Security

Resume files may contain personal information. Avoid committing resumes, local databases, API keys, environment files, or other private data to version control.

The ATS compatibility result is an estimate based on implemented checks. It is not an official score from a specific applicant tracking system and does not predict hiring outcomes.

## Current Status

CareerPilot AI runs locally. Deployment configuration and hosting requirements should be verified before publishing a live version.
