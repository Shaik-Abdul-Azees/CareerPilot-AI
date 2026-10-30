
from src.analysis.resume_analyzer import analyze_resume


def test_analyze_resume_returns_expected_fields():
    resume = """
    Bachelor of Technology in Computer Science
    Skills: Python, Java, SQL
    Experience: Software Developer Intern
    """

    result = analyze_resume(resume)

    assert isinstance(result, dict)
    assert "skills" in result
    assert "education" in result
    assert "experience" in result
    assert "word_count" in result


def test_analyze_resume_counts_words():
    resume = "Python Java SQL"

    result = analyze_resume(resume)

    assert result["word_count"] == 3


def test_analyze_resume_handles_empty_text():
    result = analyze_resume("")

    assert isinstance(result, dict)
    assert "word_count" in result



from src.analysis.resume_analyzer import analyze_ats_compatibility


def test_ats_score_is_between_zero_and_100():
    result = analyze_ats_compatibility(
        "John Doe john@example.com +1 555 123 4567 "
        "Education B.Tech Skills Python Java "
        "Experience Software Developer Projects Web App "
        + "Developed software applications. " * 60
    )

    assert 0 <= result["ats_score"] <= 100


def test_ats_score_returns_checks_and_recommendations():
    result = analyze_ats_compatibility("")

    assert "checks" in result
    assert "recommendations" in result
    assert "ats_score" in result
    assert result["ats_score"] == 0


def test_ats_score_rewards_resume_sections():
    result = analyze_ats_compatibility(
        "Contact john@example.com +1 555 123 4567 "
        "Education B.Tech Skills Python "
        "Experience Developer Projects "
        + "Built useful software. " * 60
    )

    assert result["checks"]["email"]["passed"] is True
    assert result["checks"]["education_section"]["passed"] is True
    assert result["checks"]["skills_section"]["passed"] is True
    assert result["ats_score"] > 0
