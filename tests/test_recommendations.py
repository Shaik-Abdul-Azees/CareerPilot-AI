
import json
from unittest.mock import MagicMock, patch
import urllib.error

import pytest

from src.ai.recommendations import generate_recommendations


def test_generate_recommendations_returns_text():
    fake_response = {
        "response": "## Resume Improvements\n1. Add measurable achievements."
    }

    mock_response = MagicMock()
    mock_response.__enter__.return_value.read.return_value = (
        json.dumps(fake_response).encode("utf-8")
    )

    with patch(
        "src.ai.recommendations.urllib.request.urlopen",
        return_value=mock_response,
    ) as mock_urlopen:
        result = generate_recommendations(
            resume_text="Python developer",
            job_description="Python engineer",
            matched_skills=["Python"],
            missing_skills=["Docker"],
        )

    assert isinstance(result, str)
    assert "Resume Improvements" in result
    mock_urlopen.assert_called_once()


def test_generate_recommendations_rejects_empty_response():
    fake_response = {"response": ""}

    mock_response = MagicMock()
    mock_response.__enter__.return_value.read.return_value = (
        json.dumps(fake_response).encode("utf-8")
    )

    with patch(
        "src.ai.recommendations.urllib.request.urlopen",
        return_value=mock_response,
    ):
        with pytest.raises(
            RuntimeError,
            match="returned empty recommendations",
        ):
            generate_recommendations(
                resume_text="Python developer",
                job_description="Python engineer",
                matched_skills=["Python"],
                missing_skills=["Docker"],
            )


def test_generate_recommendations_handles_connection_error():
    with patch(
        "src.ai.recommendations.urllib.request.urlopen",
        side_effect=urllib.error.URLError("Connection refused"),
    ):
        with pytest.raises(
            RuntimeError,
            match="Check that Ollama is running",
        ):
            generate_recommendations(
                resume_text="Python developer",
                job_description="Python engineer",
                matched_skills=["Python"],
                missing_skills=["Docker"],
            )
