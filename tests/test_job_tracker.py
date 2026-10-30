
import pytest

from src.database import job_tracker


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Use a separate temporary database for every test."""
    temporary_db = tmp_path / "test_jobs.db"

    monkeypatch.setattr(
        job_tracker,
        "DATABASE_PATH",
        temporary_db,
    )

    job_tracker.initialize_database()
    return temporary_db


def test_initialize_database_creates_applications_table(test_database):
    connection = job_tracker.get_connection()

    try:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'applications'
            """
        ).fetchone()

        assert result is not None
        assert result["name"] == "applications"
    finally:
        connection.close()


def test_add_and_get_application(test_database):
    job_tracker.add_application(
        company="OpenAI",
        job_title="Software Engineer",
        job_url="https://example.com/jobs/1",
        application_date="2026-10-20",
        status="Applied",
        notes="Python and backend role",
    )

    applications = job_tracker.get_applications()

    assert len(applications) == 1
    assert applications[0]["company"] == "OpenAI"
    assert applications[0]["job_title"] == "Software Engineer"
    assert applications[0]["status"] == "Applied"
    assert applications[0]["notes"] == "Python and backend role"


def test_update_application_status(test_database):
    job_tracker.add_application(
        company="Google",
        job_title="Developer",
        job_url="",
        application_date="2026-10-20",
        status="Applied",
        notes="",
    )

    application = job_tracker.get_applications()[0]

    job_tracker.update_application_status(
        application["id"],
        "Interview",
    )

    updated_applications = job_tracker.get_applications()

    assert updated_applications[0]["status"] == "Interview"


def test_invalid_status_is_rejected(test_database):
    job_tracker.add_application(
        company="Example Ltd",
        job_title="Developer",
        job_url="",
        application_date="2026-10-20",
        status="Applied",
        notes="",
    )

    application = job_tracker.get_applications()[0]

    with pytest.raises(ValueError, match="Invalid application status"):
        job_tracker.update_application_status(
            application["id"],
            "Invalid Status",
        )


def test_delete_application(test_database):
    job_tracker.add_application(
        company="Microsoft",
        job_title="Software Engineer",
        job_url="",
        application_date="2026-10-20",
        status="Applied",
        notes="",
    )

    application = job_tracker.get_applications()[0]
    job_tracker.delete_application(application["id"])

    assert job_tracker.get_applications() == []


def test_applications_are_sorted_by_date(test_database):
    job_tracker.add_application(
        company="Older Company",
        job_title="Junior Developer",
        job_url="",
        application_date="2026-10-10",
        status="Applied",
        notes="",
    )

    job_tracker.add_application(
        company="Newer Company",
        job_title="Software Engineer",
        job_url="",
        application_date="2026-10-20",
        status="Applied",
        notes="",
    )

    applications = job_tracker.get_applications()

    assert applications[0]["company"] == "Newer Company"
    assert applications[1]["company"] == "Older Company"
