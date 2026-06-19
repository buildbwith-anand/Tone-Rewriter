"""
tone_rewriter_voice.py
======================
The tone rewriter - now with VOICE input. You can type your text OR speak it.

Flow:
    speak  ->  speech-to-text  ->  existing tone rewriter  ->  llama3.2:3b

Requirements:
    1. Ollama running + model pulled (ollama pull llama3.2:3b)
    2. pip install requests SpeechRecognition pyaudio
    Note: the voice-to-text step uses Google's free service, so it needs
    internet. The rewriting itself still runs locally on your machine.
"""

import requests
import speech_recognition as sr   # NEW: handles the microphone + speech-to-text


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

# Keep your own custom tones here if you've already added some!
TONES = {
    "1": ("Professional", "formal, polished, and businesslike"),
    "2": ("Friendly",     "warm, casual, and approachable"),
    "3": ("Polite",       "courteous, gentle, and respectful"),
    "4": ("Confident",    "assertive, direct, and self-assured"),
    "5": ("Concise",      "as short and clear as possible, without losing meaning"),
    "6": ("Funny",        "humorous and playful, with light jokes or witty phrasing"),
    "7": ("Melancholic",  "wistful, reflective, and gently sad in a poetic way"),
}


# ---------------------------------------------------------------------------
# THE PROMPT
# ---------------------------------------------------------------------------
def build_system_prompt(tone_description):
    return (
        "You are a writing assistant that rewrites text in a specific tone. "
        f"Rewrite the user's message to sound {tone_description}. "
        "Keep the original meaning and all key facts intact. "
        "Return ONLY the rewritten text - no preamble, no explanation, no quotation marks."
    )


# ---------------------------------------------------------------------------
# NEW: LISTEN TO THE MICROPHONE AND RETURN TEXT
# ---------------------------------------------------------------------------
def listen():
    """Record from the mic and convert speech to text. Returns '' on failure."""
    recognizer = sr.Recognizer()          # the engine that processes audio

    with sr.Microphone() as source:       # open the default microphone
        print("\n[mic] Listening... speak now.")
        # tune out background hum for half a second so it hears you better
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source) # records until you stop talking

    print("[mic] Processing...")
    try:
        # send the audio to Google's free recognizer and get text back
        text = recognizer.recognize_google(audio)
        print(f"[mic] You said: {text}")
        return text
    except sr.UnknownValueError:
        print("[mic] Sorry, I couldn't understand that. Please try again.")
        return ""
    except sr.RequestError as error:
        print(f"[mic] Speech service error (need internet?): {error}")
        return ""


# ---------------------------------------------------------------------------
# THE CORE - send text to Ollama and get the rewrite back
# ---------------------------------------------------------------------------
def rewrite(text, tone_description):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": build_system_prompt(tone_description)},
            {"role": "user", "content": text},
        ],
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return ("ERROR: Couldn't reach Ollama. Is it running?\n"
                "Open the Ollama app, or run `ollama serve` in another terminal.")
    except requests.exceptions.RequestException as error:
        return f"ERROR talking to Ollama: {error}"
    return response.json()["message"]["content"].strip()


# ---------------------------------------------------------------------------
# THE LOOP
# ---------------------------------------------------------------------------
def main():
    print("=" * 52)
    print("   Local Tone Rewriter (with voice)  -  llama3.2:3b")
    print("=" * 52)

    while True:
        # --- get the text: typed OR spoken ---
        entry = input("\nType your text, or type 'v' to speak it (or 'q' to quit):\n> ")
        command = entry.strip().lower()

        if command in ("q", "quit", "exit"):
            print("\nGoodbye!")
            break

        if command == "v":
            text = listen()        # use the microphone
            if not text:           # if it failed, start the loop over
                continue
        elif not entry.strip():
            print("(Nothing entered - try again.)")
            continue
        else:
            text = entry           # they typed their text normally

        # --- choose a tone ---
        print("\nChoose a tone:")
        for key, (name, _description) in TONES.items():
            print(f"  {key}. {name}")
        choice = input("> ").strip()
        if choice not in TONES:
            print("(Not a valid option - using 'Professional'.)")
            choice = "1"
        tone_name, tone_description = TONES[choice]

        # --- rewrite and show ---
        print(f"\nRewriting in a {tone_name} tone...\n")
        result = rewrite(text, tone_description)
        print("-" * 52)
        print(result)
        print("-" * 52)


if __name__ == "__main__":
    main()
