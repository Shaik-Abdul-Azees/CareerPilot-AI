
from src.matching.job_matcher import match_job


def test_match_job_returns_expected_fields():
    resume = """
    Python developer with experience in Java, SQL,
    React, and REST APIs.
    """

    job_description = """
    We are looking for a developer with Python,
    Java, SQL, React, and REST APIs.
    """

    result = match_job(resume, job_description)

    assert isinstance(result, dict)
    assert "match_score" in result
    assert "matched_skills" in result
    assert "missing_skills" in result
    assert "required_skills" in result


def test_match_job_returns_valid_score():
    resume = "Python Java SQL developer"
    job_description = "Required skills: Python, Java, SQL"

    result = match_job(resume, job_description)

    assert 0 <= result["match_score"] <= 100


def test_match_job_returns_skill_lists():
    resume = "Python developer"
    job_description = "Required skills: Python, Java"

    result = match_job(resume, job_description)

    assert isinstance(result["matched_skills"], list)
    assert isinstance(result["missing_skills"], list)
    assert isinstance(result["required_skills"], list)
