# 🎓 Spanish Tutor with Ollama - Complete Documentation

A fully functional Spanish tutoring application with voice support, powered by Ollama's language models.

## ✨ Features

### Core Features
- 💬 **Natural Spanish Conversations** - Chat with an AI tutor
- 🔧 **Automatic Error Correction** - Learn from mistakes naturally
- 🎯 **B1-B2 Level Optimized** - Perfect for intermediate learners
- 🚀 **Powered by Ollama** - Uses phi3:mini, llama3.2, or mistral models
- 📊 **Clean & Minimal** - Only 6-7 core files

### Voice Features (Optional)
- 🎤 **Speech-to-Text** - Speak instead of typing
- 🔊 **Text-to-Speech** - Hear responses spoken
- 🗣️ **Multilingual** - Supports Spanish and English

## 🚀 Installation

### Quick Install (3 Steps)

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Get a model
ollama pull phi3:mini    # Fastest (2GB)
# OR
ollama pull llama3.2:3b  # Better quality (2GB)

# 3. Run the tutor
./run.sh
```

### Voice Features Setup (Optional)

```bash
# For Speech Recognition
pip install SpeechRecognition pyaudio

# For better Text-to-Speech
pip install pyttsx3 pygame
# OR
pip install edge-tts pygame  # Best quality

# Test voice features
python3 voice_handler.py
```

## 📁 Project Structure

```
spanish-tutor/
├── spanish_tutor_ollama.py  # Main application with GUI
├── voice_handler.py         # Voice input/output handler
├── test_ollama.py          # System test script
├── test_quick.py           # Quick API test
├── setup_ollama.sh         # Automated setup
├── run.sh                  # Quick launcher
├── requirements.txt        # Python dependencies
└── README.md              # This documentation
```

## 💬 Usage Examples

### Text Conversation
```
You: Hola, ¿cómo estás?
Tutor: ¡Muy bien, gracias! ¿Y tú, cómo te va con el español?

You: Ayer he yendo al mercado
Tutor: Ah, qué bien. Por cierto, se dice "he ido" no "he yendo". ¿Qué compraste?
```

### Voice Interaction
1. Click "🎤 Hablar" button
2. Speak in Spanish or English
3. Tutor responds with voice

## 🎮 Keyboard Shortcuts

- **Enter** - Send message
- **Ctrl+L** - Clear conversation
- **Ctrl+M** - Change model
- **Ctrl+Q** - Quit

## 🔧 Configuration

### Change Spanish Voice
Edit `spanish_tutor_ollama.py`:
```python
TTS_VOICE = "es-ES-AlvaroNeural"  # Male
# OR
TTS_VOICE = "es-ES-ElviraNeural"  # Female
```

### Adjust Microphone Sensitivity
Edit `voice_handler.py`:
```python
self.recognizer.energy_threshold = 3000  # Higher = less sensitive
```

### Change Response Length
Edit `spanish_tutor_ollama.py`:
```python
"num_predict": 150,  # Increase for longer responses
```

## 🧪 Testing

### Test Complete System
```bash
python3 test_ollama.py
```

### Test Voice Only
```bash
python3 voice_handler.py
```

### Test Ollama API
```bash
python3 test_quick.py
```

## 📊 Performance Tips

1. **First response is slow** (model loading) - normal!
2. **phi3:mini** - Fastest responses
3. **llama3.2:3b** - Better quality
4. **mistral:7b** - Best quality, slower

## 🐛 Troubleshooting

### Ollama Issues
```bash
# Check if running
curl http://localhost:11434

# Start manually
ollama serve

# List models
ollama list
```

### Microphone Not Working
```bash
# Test microphone
arecord -l  # List devices
arecord -d 5 test.wav  # Record 5 seconds
```

### No Sound Output
```bash
# Test speakers
espeak "Hello"

# Check volume
alsamixer
```

## 🌟 Advanced Features

### Add Custom Corrections
Edit `detect_errors()` in `spanish_tutor_ollama.py`:
```python
error_patterns = {
    "your_pattern": "correction",
    # Add more...
}
```

### Change System Prompt
Edit `self.system_prompt` to customize tutor personality.

## 📚 Learning Tips

1. **Start Simple** - Basic greetings and introductions
2. **Make Mistakes** - The tutor will correct you naturally
3. **Ask Questions** - "¿Cómo se dice...?" "¿Qué significa...?"
4. **Practice Daily** - Even 10 minutes helps
5. **Use Voice** - Speaking improves pronunciation

## 🚀 Future Enhancements

- [ ] Save conversation history
- [ ] Track learning progress
- [ ] Add grammar exercises
- [ ] Support more languages
- [ ] Mobile app version

## 📝 License

Open source - Feel free to modify and share!

## 🙏 Credits

- **Ollama** - Local LLM inference
- **phi3:mini** - Microsoft's efficient model
- **Python Community** - Amazing libraries

---

**¡Disfruta aprendiendo español!** 🇪🇸

For issues or questions, check the troubleshooting section or create an issue.
