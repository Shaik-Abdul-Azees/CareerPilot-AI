
import re

from src.analysis.resume_analyzer import find_skills


def normalize_skill(skill: str) -> str:
    """Normalize skill names for comparison."""
    return skill.lower().strip()


def match_job(resume_text: str, job_description: str) -> dict:
    """Compare resume skills against skills found in a job description."""

    resume_categories = find_skills(resume_text)
    job_categories = find_skills(job_description)

    resume_skills = {
        normalize_skill(skill)
        for skills in resume_categories.values()
        for skill in skills
    }

    required_skills = {
        normalize_skill(skill)
        for skills in job_categories.values()
        for skill in skills
    }

    matched = sorted(resume_skills & required_skills)
    missing = sorted(required_skills - resume_skills)

    if required_skills:
        score = round(len(matched) / len(required_skills) * 100)
    else:
        score = 0

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(required_skills),
    }
