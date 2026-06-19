import speech_recognition as sr


def listen():
    """Record from the mic and return transcribed text, or '' on failure."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n[mic] Listening... speak now.")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    print("[mic] Processing...")
    try:
        text = recognizer.recognize_google(audio)
        print(f"[mic] You said: {text}")
        return text
    except sr.UnknownValueError:
        print("[mic] Sorry, I couldn't understand that. Please try again.")
        return ""
    except sr.RequestError as error:
        print(f"[mic] Speech service error (need internet?): {error}")
        return ""
