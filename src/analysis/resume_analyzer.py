
import re


SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C", "SQL"
    ],
    "Web Development": [
        "HTML", "CSS", "React", "Next.js", "Node.js",
        "Express.js", "Bootstrap", "Tailwind CSS", "REST API"
    ],
    "Databases": [
        "MySQL", "MongoDB", "PostgreSQL", "SQLite", "Redis"
    ],
    "AI and Machine Learning": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence",
        "TensorFlow", "PyTorch", "Scikit-learn", "NLP",
        "Natural Language Processing", "Generative AI", "RAG",
        "Sentence Transformers", "FAISS"
    ],
    "Cloud and Tools": [
        "AWS", "Azure", "Docker", "Git", "GitHub", "Linux",
        "FastAPI", "Flask", "Streamlit", "Spring Boot"
    ],
}


def find_skills(resume_text: str) -> dict:
    """Find known technical skills mentioned in resume text."""
    detected = {}

    for category, skills in SKILL_CATEGORIES.items():
        matches = []

        for skill in skills:
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

            if re.search(pattern, resume_text, re.IGNORECASE):
                matches.append(skill)

        if matches:
            detected[category] = matches

    return detected


def find_education(resume_text: str) -> list:
    """Find common education keywords in resume text."""
    education_terms = [
        "B.Tech", "B.E.", "B.Sc", "BCA", "M.Tech", "M.E.",
        "M.Sc", "MCA", "Bachelor", "Master", "Ph.D.",
        "Intermediate", "Higher Secondary", "Diploma", "CGPA"
    ]

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    results = []

    for line in lines:
        if any(
            re.search(re.escape(term), line, re.IGNORECASE)
            for term in education_terms
        ):
            results.append(line)

    return results[:15]


def find_experience(resume_text: str) -> list:
    """Find lines that may describe work or project experience."""
    experience_terms = [
        "intern", "experience", "developer", "engineer",
        "worked", "developed", "built", "project",
        "responsibilities", "employment"
    ]

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    results = []

    for line in lines:
        if any(term in line.lower() for term in experience_terms):
            results.append(line)

    return results[:20]


def analyze_resume(resume_text: str) -> dict:
    """Return a basic analysis of extracted resume text."""
    return {
        "skills": find_skills(resume_text),
        "education": find_education(resume_text),
        "experience": find_experience(resume_text),
        "word_count": len(resume_text.split()),
    }



def analyze_ats_compatibility(resume_text: str) -> dict:
    """Estimate ATS compatibility using text-based resume checks.

    This is a heuristic score, not a prediction from any specific ATS.
    """
    text = resume_text.strip()
    lower_text = text.lower()
    word_count = len(text.split())

    checks = {}
    recommendations = []

    # 1. Email address: 10 points
    has_email = bool(
        re.search(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
                  text, re.IGNORECASE)
    )
    checks["email"] = {
        "passed": has_email,
        "points": 10 if has_email else 0,
        "max_points": 10,
    }
    if not has_email:
        recommendations.append(
            "Add a professional email address to your resume."
        )

    # 2. Phone number: 10 points
    has_phone = bool(
        re.search(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)", text)
    )
    checks["phone"] = {
        "passed": has_phone,
        "points": 10 if has_phone else 0,
        "max_points": 10,
    }
    if not has_phone:
        recommendations.append(
            "Add a contact phone number if appropriate."
        )

    # 3. Education section: 15 points
    has_education = bool(
        re.search(
            r"\b(education|academic background|qualifications)\b",
            lower_text,
        )
    )
    checks["education_section"] = {
        "passed": has_education,
        "points": 15 if has_education else 0,
        "max_points": 15,
    }
    if not has_education:
        recommendations.append(
            "Add a clearly labeled Education section."
        )

    # 4. Experience section: 15 points
    has_experience = bool(
        re.search(
            r"\b(experience|work history|employment|internships?)\b",
            lower_text,
        )
    )
    checks["experience_section"] = {
        "passed": has_experience,
        "points": 15 if has_experience else 0,
        "max_points": 15,
    }
    if not has_experience:
        recommendations.append(
            "Add a clearly labeled Experience or Internship section "
            "if relevant to your background."
        )

    # 5. Skills section: 15 points
    has_skills_section = bool(
        re.search(r"\b(technical skills|skills|core competencies)\b",
                  lower_text)
    )
    checks["skills_section"] = {
        "passed": has_skills_section,
        "points": 15 if has_skills_section else 0,
        "max_points": 15,
    }
    if not has_skills_section:
        recommendations.append(
            "Add a clearly labeled Skills section."
        )

    # 6. Projects section: 10 points
    has_projects = bool(
        re.search(r"\b(projects|personal projects|academic projects)\b",
                  lower_text)
    )
    checks["projects_section"] = {
        "passed": has_projects,
        "points": 10 if has_projects else 0,
        "max_points": 10,
    }
    if not has_projects:
        recommendations.append(
            "Consider adding a Projects section with relevant work."
        )

    # 7. Text length: 15 points
    if 200 <= word_count <= 1000:
        length_points = 15
        good_length = True
    elif 100 <= word_count < 200 or 1000 < word_count <= 1500:
        length_points = 8
        good_length = False
    else:
        length_points = 0
        good_length = False

    checks["text_length"] = {
        "passed": good_length,
        "points": length_points,
        "max_points": 15,
        "word_count": word_count,
    }
    if not good_length:
        recommendations.append(
            "Review resume length and remove unnecessary content. "
            "These word-count ranges are guidelines, not strict rules."
        )

    # 8. Usable extracted text: 10 points
    has_readable_text = word_count >= 50
    checks["readable_text"] = {
        "passed": has_readable_text,
        "points": 10 if has_readable_text else 0,
        "max_points": 10,
    }
    if not has_readable_text:
        recommendations.append(
            "Check that your PDF contains selectable text and that "
            "the resume content was extracted correctly."
        )

    score = sum(check["points"] for check in checks.values())

    return {
        "ats_score": score,
        "checks": checks,
        "recommendations": recommendations,
        "word_count": word_count,
        "score_type": "Heuristic ATS compatibility estimate",
    }
