import json
import requests

from .config import OLLAMA_URL, MODEL


def _build_system_prompt(tone_description):
    return (
        "You are a writing assistant that rewrites text in a specific tone. "
        f"Rewrite the user's message to sound {tone_description}. "
        "Keep the original meaning and all key facts intact. "
        "Return ONLY the rewritten text - no preamble, no explanation, no quotation marks."
    )


def _payload(text, tone_description, stream=False):
    return {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": _build_system_prompt(tone_description)},
            {"role": "user",   "content": text},
        ],
        "stream": stream,
    }


def rewrite(text, tone_description):
    try:
        response = requests.post(OLLAMA_URL, json=_payload(text, tone_description), timeout=120)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return (
            "ERROR: Could not reach Ollama. Is it running?\n"
            "Open the Ollama app, or run `ollama serve` in another terminal."
        )
    except requests.exceptions.RequestException as error:
        return f"ERROR talking to Ollama: {error}"
    return response.json()["message"]["content"].strip()


def rewrite_stream(text, tone_description):
    """Yield text chunks from Ollama's streaming response."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json=_payload(text, tone_description, stream=True),
            stream=True,
            timeout=120,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        yield "ERROR: Could not reach Ollama. Is it running?"
        return
    except requests.exceptions.RequestException as error:
        yield f"ERROR talking to Ollama: {error}"
        return

    for line in response.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        token = chunk.get("message", {}).get("content", "")
        if token:
            yield token
        if chunk.get("done"):
            break
