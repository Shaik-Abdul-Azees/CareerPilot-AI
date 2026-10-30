
import json
import urllib.error
import urllib.request
import socket


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def generate_recommendations(
    resume_text: str,
    job_description: str,
    matched_skills: list,
    missing_skills: list,
) -> str:
    """Generate career recommendations using local Ollama."""

    prompt = f"""
You are a practical career assistant.

Analyze the resume and job description below.

RESUME:
{resume_text[:6000]}

JOB DESCRIPTION:
{job_description[:4000]}

MATCHING SKILLS:
{", ".join(matched_skills) if matched_skills else "None detected"}

MISSING OR UNDETECTED SKILLS:
{", ".join(missing_skills) if missing_skills else "None detected"}

Provide:
1. Three resume improvement suggestions.
2. Three skills to prioritize learning.
3. Five technical interview questions with brief answers.
4. Two relevant project ideas.

Do not invent qualifications or claim that the candidate has
skills not supported by the resume. A skill not detected in
the text does not necessarily mean the candidate lacks it.

Use clear headings and practical recommendations.
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=300,
        ) as response:
            result = json.loads(response.read().decode("utf-8"))

        generated_text = result.get("response", "").strip()

        if not generated_text:
            raise RuntimeError(
                "Ollama responded, but returned empty recommendations."
            )

        return generated_text

    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Ollama returned HTTP {error.code}: {details}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Could not connect to Ollama at {OLLAMA_URL}. "
            f"Connection details: {error.reason}. "
            "Check that Ollama is running."
        ) from error

    except (TimeoutError, socket.timeout) as error:
        raise RuntimeError(
            "Ollama did not finish within 300 seconds. "
            "Try again with a shorter resume or job description."
        ) from error

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Ollama returned a response that could not be decoded."
        ) from error
