# 🎉 Spanish Tutor - Complete Setup Guide

## ✅ What's Been Done

### 1. **Updated Core Files**
- ✅ `run.sh` - Now has interactive menu to choose versions
- ✅ `spanish_tutor_improved.py` - MAIN VERSION with all fixes
- ✅ `voice_config.py` - Full voice configuration tool
- ✅ `voice_playground.py` - Easy voice parameter testing

### 2. **Organization Tools**
- ✅ `cleanup.sh` - Organizes project structure
- ✅ `quick_fix.sh` - Fixes common issues

## 🎯 How to Play with Voice Parameters

### Method 1: Voice Playground (EASIEST)
```bash
# Interactive menu
python3 voice_playground.py

# Quick tests
python3 voice_playground.py --slow    # Clear & slow
python3 voice_playground.py --normal  # Balanced
python3 voice_playground.py --fast    # Natural speed

# Custom parameters
python3 voice_playground.py 110 50 12  # speed pitch gap
```

### Method 2: Voice Config Tool (ADVANCED)
```bash
python3 voice_config.py

# Menu options:
# 1) Adjust SPEED (50-200)
# 2) Adjust PITCH (0-100)  
# 3) Adjust WORD GAP (0-50ms)
# 4) Change VOICE (spanish-latin-am, es, es+f3, etc)
# 5) Test phrases
```

### Method 3: Direct Testing (MANUAL)
```bash
# Format: espeak -v VOICE -s SPEED -p PITCH -g GAP "text"

# Super clear for beginners
espeak -v spanish-latin-am -s 90 -p 50 -g 20 "Hola, ¿cómo estás?"

# Balanced (recommended)
espeak -v spanish-latin-am -s 120 -p 50 -g 10 "Buenos días"

# Natural native speed
espeak -v spanish-latin-am -s 150 -p 45 -g 5 "¿Qué tal?"

# Female voice
espeak -v es+f3 -s 110 -p 60 -g 12 "Me llamo María"

# Deep male voice
espeak -v es+m1 -s 100 -p 30 -g 15 "Soy profesor"
```

## 📊 Voice Parameter Guide

### Speed (-s)
- **50-80**: Very fast (hard to understand)
- **90-110**: Clear and slow (beginners) ⭐
- **120-130**: Natural pace (intermediate) ⭐
- **140-160**: Native speed (advanced)
- **170-200**: Very slow (too slow usually)

### Pitch (-p)
- **0-30**: Deep voice (masculine)
- **40-60**: Natural range ⭐
- **70-100**: High voice (feminine/child-like)

### Word Gap (-g)
- **0-5**: No gaps (fluent but less clear)
- **8-12**: Natural pauses ⭐
- **15-20**: Clear separation (learning)
- **25-50**: Too much gap (robotic)

### Best Voices
1. **spanish-latin-am** - Clearest pronunciation ⭐
2. **es** - Standard Spanish
3. **es+f3** - Female variant
4. **es+m1** - Male variant

## 🚀 Quick Start Commands

### 1. Run the Tutor
```bash
# Interactive menu (choose version)
./run.sh

# Direct launch (best version)
python3 spanish_tutor_improved.py
```

### 2. Configure Voice
```bash
# Find your perfect voice
python3 voice_playground.py

# Save configuration
python3 voice_config.py
```

### 3. Test Components
```bash
# Test voice recognition
python3 test_voice.py

# Test TTS options
python3 test_tts.py
```

## 🧹 Clean Up Project
```bash
# Organize files into folders
./cleanup.sh

# This will:
# - Move old versions → old_versions/
# - Move docs → docs/
# - Move tests → tests/
# - Create new README
```

## 💡 Pro Tips

### For Clearest TTS:
1. **Speed**: 100-120 (slower = clearer)
2. **Voice**: spanish-latin-am
3. **Gap**: 10-15ms
4. **Install pyttsx3**: `pip install pyttsx3`

### Best Learning Settings:
```bash
# Beginner
espeak -v spanish-latin-am -s 100 -p 50 -g 15

# Intermediate  
espeak -v spanish-latin-am -s 120 -p 50 -g 10

# Advanced
espeak -v spanish-latin-am -s 140 -p 45 -g 5
```

### Voice Recognition Tips:
- Speak complete sentences
- Say "Me llamo..." not just name
- Reduce background noise
- Watch status indicators

## 📁 Current Files

### Core Application
- `spanish_tutor_improved.py` - MAIN APP (use this!)
- `voice_handler.py` - Voice utilities
- `run.sh` - Launch script

### Configuration Tools
- `voice_playground.py` - Test voice parameters
- `voice_config.py` - Advanced configuration
- `quick_fix.sh` - Fix common issues

### Old Versions (for reference)
- `spanish_tutor_integrated.py` - Basic voice version
- `spanish_tutor_ollama.py` - Original version
- `spanish_tutor_ollama_backup.py` - Your backup

### Tests
- `test_voice.py` - Test speech recognition
- `test_tts.py` - Test TTS engines
- `test_quick.py` - Test Ollama

## 🎮 Try This Now!

### 1. Test Voice Settings
```bash
# Compare different speeds
python3 voice_playground.py
# Choose option 1 (Quick Comparison)
```

### 2. Find Your Voice
```bash
# Test different voices
python3 voice_playground.py
# Choose option 2 (Voice Showcase)
```

### 3. Interactive Tuning
```bash
# Fine-tune parameters
python3 voice_playground.py
# Choose option 3 (Interactive)
# Try: s100, p60, g15, test
```

### 4. Run the Tutor
```bash
./run.sh
# Choose 1 for improved version
```

## 🆘 Troubleshooting

### TTS Still Unclear?
```bash
# Try female voice
espeak -v es+f3 -s 110 -p 55 -g 12 "Prueba de voz"

# Or install pyttsx3
pip install --user pyttsx3
```

### Voice Not Working?
```bash
# Install dependencies
./setup_voice.sh

# Test microphone
python3 test_voice.py
```

## ✨ Summary

You now have:
1. **Improved Tutor** with better TTS and shorter responses
2. **Voice Playground** to test parameters easily
3. **Voice Config Tool** for advanced settings
4. **Updated run.sh** with menu system
5. **Cleanup script** to organize files

Just run `./run.sh` and choose option 1 for the best experience!

For voice tuning, use `python3 voice_playground.py` - it's the easiest way to find your perfect Spanish voice settings.
