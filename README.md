# 🎙️ Tone Rewriter (with Voice Input)

A Python CLI tool that rewrites your text — or spoken words — in any tone you choose.  
Powered by **Ollama** running locally on your machine. No cloud LLM. No API costs. No data leaving your device.

---

## ✨ Features

- 🎤 **Voice input** — speak naturally, it transcribes for you
- ⌨️ **Type input** — paste or type any text directly
- 🎭 **7 built-in tones** — Professional, Friendly, Polite, Confident, Concise, Funny, Melancholic
- 🔒 **100% local LLM** — rewriting runs on your machine via Ollama
- 🪶 **Lightweight** — single Python file, minimal dependencies

---

## 🖥️ Demo

```
====================================================
   Local Tone Rewriter (with voice)  -  llama3.2:3b
====================================================

Type your text, or type 'v' to speak it (or 'q' to quit):
> v

[mic] Listening... speak now.
[mic] Processing...
[mic] You said: i cant make it to the meeting tomorrow something came up

Choose a tone:
  1. Professional
  2. Friendly
  3. Polite
  4. Confident
  5. Concise
  6. Funny
  7. Melancholic
> 1

Rewriting in a Professional tone...

----------------------------------------------------
Unfortunately, I will be unable to attend tomorrow's meeting due to an unforeseen circumstance. 
I apologize for any inconvenience this may cause.
----------------------------------------------------
```

---

## 📦 Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed and running
- `llama3.2:3b` model pulled
- Internet connection *(only for speech-to-text via Google's free API)*

---

## 🚀 Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/tone-rewriter.git
cd tone-rewriter
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

> **On Linux**, you may need to install `portaudio` first:
> ```bash
> sudo apt install portaudio19-dev
> ```
> **On Mac:**
> ```bash
> brew install portaudio
> ```

### 3. Install and start Ollama

Download Ollama from [ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before you launch the script. Either open the Ollama desktop app, or run:

```bash
ollama serve
```

### 4. Run it

```bash
python tone_rewriter_voice.py
```

---

## 🎭 Available Tones

| # | Tone | Description |
|---|------|-------------|
| 1 | Professional | Formal, polished, and businesslike |
| 2 | Friendly | Warm, casual, and approachable |
| 3 | Polite | Courteous, gentle, and respectful |
| 4 | Confident | Assertive, direct, and self-assured |
| 5 | Concise | As short and clear as possible |
| 6 | Funny | Humorous and playful |
| 7 | Melancholic | Wistful, reflective, and poetic |

---

## 🛠️ How It Works

```
[You speak or type]
        ↓
[Google Speech-to-Text API]   ← needs internet (free)
        ↓
[Ollama (llama3.2:3b) locally rewrites the tone]
        ↓
[Output shown in terminal]
```

The **speech-to-text** step uses Google's free recognition service (internet required).  
The **tone rewriting** step runs entirely on your machine via Ollama — offline, private, and free.

---

## ➕ Adding Custom Tones

Open `tone_rewriter_voice.py` and add a new entry to the `TONES` dictionary:

```python
TONES = {
    ...
    "8": ("Sarcastic", "dry, ironic, and subtly sarcastic"),
}
```

---

## 🔧 Switching the Model

The default model is `llama3.2:3b`. To use a different Ollama model, change the `MODEL` constant at the top of the file:

```python
MODEL = "llama3.2:3b"   # change this to e.g. "mistral", "gemma3", etc.
```

Then pull your chosen model: `ollama pull mistral`

---

## 📁 Project Structure

```
tone-rewriter/
├── tone_rewriter_voice.py   # main script
├── requirements.txt         # Python dependencies
└── README.md                # this file
```

---

## 🤝 Contributing

Contributions are welcome! Ideas:
- Add more tones
- Support saving output to a file
- Add a `--tone` CLI flag to skip the menu
- Add offline STT (e.g. Whisper)

Feel free to open an issue or submit a PR.

---

## 📄 License

MIT License — free to use, modify, and share.

---

## 🙏 Built With

- [Ollama](https://ollama.com) — local LLM runner
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — voice input
- [PyAudio](https://pypi.org/project/PyAudio/) — microphone access
- [Requests](https://pypi.org/project/requests/) — HTTP calls to Ollama
