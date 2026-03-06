```markdown
# 🎓 AI Spanish Tutor (Local LLM & Voice)

A privacy-first, locally hosted Spanish language tutor designed for English speakers. Built with Python and Tkinter, it uses local Large Language Models (via Ollama) and speech recognition to simulate natural, conversational language practice. 

The application is heavily optimized for desktop usage, featuring Push-to-Talk, full GPU offloading, and automatic memory management.

## ✨ Features

* 🗣️ **Voice Interaction:** Native Speech-to-Text (STT) and Text-to-Speech (TTS) for hands-free practice.
* 🎙️ **Push-to-Talk (PTT):** Use the `F2` key to seamlessly trigger the microphone while the window is focused.
* 🧠 **Local AI:** Powered by [Ollama](https://ollama.com/), ensuring your conversations never leave your machine.
* 🚀 **GPU Accelerated:** Automatically requests full GPU offloading (`num_gpu: -1`) for near-instant responses.
* 🧹 **VRAM Management:** Gracefully unloads the model from your GPU memory when the application is closed.
* 🔄 **Dynamic Model Switching:** Switch between installed Ollama models (e.g., Llama 3.2, StableLM) on the fly via the top menu.
* 💾 **Save/Load Sessions:** Export your conversation history to JSON for later review.

## 🛠️ Prerequisites

1. **Ollama:** Must be installed and running (`ollama serve`).
2. **LLM Models:** Pull at least one instruction-tuned model. Llama 3.2 is highly recommended for Spanish:
   ```bash
   ollama pull llama3.2:3b

```

3. **Linux System Audio Packages:** PyAudio and TTS engines require underlying system libraries. On Debian/Ubuntu-based systems (or equivalent on your distribution):
```bash
sudo apt-get install python3-pyaudio portaudio19-dev espeak espeak-ng

```



## 📦 Installation

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/spanish-tutor.git](https://github.com/yourusername/spanish-tutor.git)
cd spanish-tutor

```


2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate

```


3. Install the required Python packages:
```bash
pip install requests SpeechRecognition pyaudio pyttsx3

```



## 🚀 Usage

Start the application:

```bash
python3 spanish_tutor_improved.py

```

1. **Select a Model:** Choose your preferred Ollama model from the prompt or the "Settings" menu.
2. **Speak:** Press and hold **`F2`** to speak, or click the "🎤 Speak" button.
3. **Listen:** The tutor will respond in text and read the response aloud automatically.
4. **Repeat:** Missed what the tutor said? Click the "🔁 Repeat" button.

## ⚠️ Pro-Tip for Linux Users (Silencing ALSA Errors)

If you see a lot of harmless `ALSA lib pcm_dsnoop.c` errors in your terminal when the app starts listening, this is just PyAudio polling your hardware channels. To run the app with a clean terminal, you can redirect standard error to `/dev/null`:

```bash
python3 spanish_tutor_improved.py 2> /dev/null

```

## 📄 License

MIT License
