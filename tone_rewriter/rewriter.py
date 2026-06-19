import requests

from .config import OLLAMA_URL, MODEL


def _build_system_prompt(tone_description):
    return (
        "You are a writing assistant that rewrites text in a specific tone. "
        f"Rewrite the user's message to sound {tone_description}. "
        "Keep the original meaning and all key facts intact. "
        "Return ONLY the rewritten text - no preamble, no explanation, no quotation marks."
    )


def rewrite(text, tone_description):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": _build_system_prompt(tone_description)},
            {"role": "user",   "content": text},
        ],
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return (
            "ERROR: Could not reach Ollama. Is it running?\n"
            "Open the Ollama app, or run `ollama serve` in another terminal."
        )
    except requests.exceptions.RequestException as error:
        return f"ERROR talking to Ollama: {error}"
    return response.json()["message"]["content"].strip()
