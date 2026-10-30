
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parents[2] / "jobs.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the applications table if it does not exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                job_title TEXT NOT NULL,
                job_url TEXT DEFAULT '',
                application_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied',
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def add_application(
    company,
    job_title,
    job_url,
    application_date,
    status,
    notes,
):
    """Save a job application."""
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO applications
            (company, job_title, job_url, application_date, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                company,
                job_title,
                job_url,
                application_date,
                status,
                notes,
            ),
        )


def get_applications():
    """Return all applications, newest application date first."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM applications
            ORDER BY application_date DESC, id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def update_application_status(application_id, new_status):
    """Update the status of an existing application."""
    allowed_statuses = {
        "Interested",
        "Applied",
        "Assessment",
        "Interview",
        "Offer",
        "Rejected",
        "Withdrawn",
    }

    if new_status not in allowed_statuses:
        raise ValueError("Invalid application status.")

    with get_connection() as connection:
        connection.execute(
            "UPDATE applications SET status = ? WHERE id = ?",
            (new_status, application_id),
        )


def delete_application(application_id):
    """Delete an application by its ID."""
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM applications WHERE id = ?",
            (application_id,),
        )


initialize_database()
