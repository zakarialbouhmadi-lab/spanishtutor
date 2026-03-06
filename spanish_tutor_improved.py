#!/usr/bin/env python3
"""
Spanish Tutor with Ollama - Improved Voice & TTS
English UI, GPU Offloading, and Memory Management
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import json
import requests
import subprocess
from datetime import datetime
import os
import queue

# Import voice handler
try:
    import speech_recognition as sr

    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False
    print("⚠️ Speech recognition not available. Install: pip install SpeechRecognition pyaudio")

# Try pyttsx3 for better TTS
try:
    import pyttsx3

    engine = pyttsx3.init()
    # Configure for Spanish
    voices = engine.getProperty('voices')
    spanish_voice = None
    for voice in voices:
        if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
            spanish_voice = voice.id
            break
    if spanish_voice:
        engine.setProperty('voice', spanish_voice)
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1.0)
    PYTTSX3_AVAILABLE = True
    print("✅ pyttsx3 TTS ready")
except:
    PYTTSX3_AVAILABLE = False
    print("⚠️ pyttsx3 not available, using espeak")


class ImprovedSpanishTutor:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Spanish Tutor")
        self.root.geometry("800x650")

        # Configuration
        self.model_name = "stablelm2:1.6b"
        self.ollama_chat_api = "http://localhost:11434/api/chat"
        self.ollama_generate_api = "http://localhost:11434/api/generate"
        self.max_context_length = 20  # Warning threshold

        # State
        self.is_listening = False
        self.conversation_history = []
        self.tts_enabled = True

        # Voice setup
        self.recognizer = None
        if STT_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 3000
            self.recognizer.pause_threshold = 0.8
            print("✅ Voice recognition ready")

        # System prompt - Updated to allow longer answers and instruct in English
        self.system_prompt = """You are a Spanish language tutor for an English-speaking student. 

STRICT RULES:
1. Always respond in Spanish to maintain immersion.
2. Be natural, helpful, and conversational.
3. Subtly correct the user's Spanish grammar or vocabulary if they make mistakes.
4. You may provide very brief English translations ONLY if explaining a complex grammatical concept, but default to Spanish.
5. Keep the conversation engaging by asking follow-up questions."""

        # Check Ollama
        self.ollama_available = self.check_ollama()

        # Create GUI
        self.create_gui()

        # Bind F2 key for Push-to-Talk
        self.root.bind_all('<F2>', lambda e: self.toggle_voice_recording())

        # Bind window close event to unload model
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Welcome message
        self.root.after(500, self.send_welcome)

    def check_ollama(self):
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                models_data = response.json().get('models', [])
                self.available_models = [m['name'] for m in models_data]

                if self.available_models:
                    self.model_name = self.available_models[0]
                    print(f"✅ Ollama running with models: {self.available_models}")
                    return True
                else:
                    print("❌ No models installed.")
                    return False
        except:
            print("❌ Ollama not running. Start with: ollama serve")
            return False
        return False

    def create_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.status_label = ttk.Label(status_frame, text="🟢 Ready (Press F2 to speak)", foreground="green")
        self.status_label.pack(side=tk.LEFT)

        self.tts_var = tk.BooleanVar(value=True)
        self.tts_checkbox = ttk.Checkbutton(
            status_frame, text="🔊 Voice Enabled", variable=self.tts_var, command=self.toggle_tts
        )
        self.tts_checkbox.pack(side=tk.RIGHT, padx=10)

        # Conversation display
        self.conversation_text = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=70, height=25, font=("Arial", 11), bg="#f5f5f5"
        )
        self.conversation_text.grid(row=1, column=0, pady=10)
        self.conversation_text.tag_config("user", foreground="#0066cc", font=("Arial", 11, "bold"))
        self.conversation_text.tag_config("tutor", foreground="#009900", font=("Arial", 11))
        self.conversation_text.tag_config("system", foreground="#666666", font=("Arial", 10, "italic"))
        self.conversation_text.tag_config("warning", foreground="#cc6600", font=("Arial", 10, "bold"))

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))

        self.input_text = ttk.Entry(input_frame, font=("Arial", 11), width=50)
        self.input_text.grid(row=0, column=0, padx=(0, 5))
        self.input_text.bind("<Return>", lambda e: self.send_message())

        self.send_button = ttk.Button(input_frame, text="📤 Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=2)

        self.voice_button = ttk.Button(
            input_frame, text="🎤 Speak (F2)", command=self.toggle_voice_recording
        )
        self.voice_button.grid(row=0, column=2, padx=2)

        if not STT_AVAILABLE:
            self.voice_button.config(state="disabled", text="🔇 Unavailable")

        self.tts_button = ttk.Button(input_frame, text="🔁 Repeat", command=self.speak_last)
        self.tts_button.grid(row=0, column=3, padx=2)

        self.clear_button = ttk.Button(input_frame, text="🗑️ Clear", command=self.clear_conversation)
        self.clear_button.grid(row=0, column=4, padx=2)

        # Menu bar (Translated to English)
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="💾 Save", command=self.save_conversation)
        file_menu.add_command(label="📂 Load", command=self.load_conversation)
        file_menu.add_separator()
        file_menu.add_command(label="❌ Exit", command=self.on_closing)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="🤖 Change Model", command=self.select_model_dialog)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="📊 Statistics", command=self.show_stats)
        help_menu.add_command(label="⚙️ TTS Config", command=self.configure_tts)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.input_text.focus()

    def on_closing(self):
        """Unload the model from VRAM and close the application"""
        self.status_label.config(text="🛑 Shutting down and unloading model...", foreground="red")
        self.root.update()

        if self.model_name:
            try:
                # Setting keep_alive to 0 forces Ollama to unload the model from memory
                requests.post(
                    self.ollama_generate_api,
                    json={
                        "model": self.model_name,
                        "keep_alive": 0
                    },
                    timeout=3
                )
                print(f"✅ Unloaded model {self.model_name} from memory.")
            except Exception as e:
                print(f"⚠️ Could not unload model: {e}")

        self.root.destroy()

    def toggle_tts(self):
        self.tts_enabled = self.tts_var.get()
        status = "Enabled" if self.tts_enabled else "Disabled"
        self.add_message("System", f"Voice {status}", "system")

    def send_welcome(self):
        if not self.model_name:
            self.add_message("System", "⚠️ No Ollama models installed.", "system")
            return

        if len(self.available_models) > 1:
            self.select_model_dialog()

        welcome = "¡Hola! Soy tu tutor de español. ¿Cómo te llamas?"
        self.add_message("Tutor", welcome, "tutor")
        self.speak_text(welcome)

    def select_model_dialog(self):
        if len(self.available_models) <= 1:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Select Model")
        dialog.geometry("400x300")
        dialog.transient(self.root)

        tk.Label(dialog, text="Available Models:", font=("Arial", 12, "bold")).pack(pady=10)
        var = tk.StringVar(value=self.model_name)

        for model in self.available_models:
            tk.Radiobutton(dialog, text=model, variable=var, value=model, font=("Arial", 10)).pack(anchor=tk.W, padx=20)

        def apply_model():
            self.model_name = var.get()
            print(f"✅ Using model: {self.model_name}")
            self.add_message("System", f"Model changed to: {self.model_name}", "system")
            dialog.destroy()

        tk.Button(dialog, text="Use this model", command=apply_model).pack(pady=20)

    def add_message(self, sender, message, tag="user"):
        self.conversation_text.config(state=tk.NORMAL)
        self.conversation_text.insert(tk.END, f"{sender}: ", tag)
        self.conversation_text.insert(tk.END, f"{message}\n\n")
        self.conversation_text.config(state=tk.DISABLED)
        self.conversation_text.see(tk.END)

    def toggle_voice_recording(self):
        if not STT_AVAILABLE:
            messagebox.showwarning("Error", "Please install: pip install SpeechRecognition pyaudio")
            return

        if not self.is_listening:
            self.is_listening = True
            self.voice_button.config(text="⏹️ Stop")
            self.status_label.config(text="🎤 Listening...", foreground="red")
            threading.Thread(target=self.record_and_process_speech, daemon=True).start()
        else:
            self.is_listening = False
            self.voice_button.config(text="🎤 Speak (F2)")
            self.status_label.config(text="🟢 Ready (Press F2 to speak)", foreground="green")

    def record_and_process_speech(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=8)
                self.root.after(0, lambda: self.status_label.config(text="🔄 Processing...", foreground="blue"))

                text = ""
                try:
                    text = self.recognizer.recognize_google(audio, language="es-ES")
                except:
                    try:
                        text = self.recognizer.recognize_google(audio, language="es-MX")
                    except:
                        pass

                if text:
                    self.root.after(0, lambda: self.process_voice_input(text))
                else:
                    self.root.after(0, lambda: self.status_label.config(text="❌ Didn't catch that", foreground="red"))

        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.status_label.config(text="⏱️ No audio detected", foreground="orange"))
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="❌ Audio error", foreground="red"))
        finally:
            self.is_listening = False
            self.root.after(0, lambda: self.voice_button.config(text="🎤 Speak (F2)"))
            time.sleep(1.5)
            self.root.after(0, lambda: self.status_label.config(text="🟢 Ready (Press F2 to speak)", foreground="green"))

    def process_voice_input(self, text):
        self.input_text.delete(0, tk.END)
        self.input_text.insert(0, text)
        self.root.update()
        time.sleep(0.5)
        self.send_message()

    def get_ollama_response(self, user_input):
        messages = [{"role": "system", "content": self.system_prompt}]

        # Load full history, but warn if it gets too long
        for msg in self.conversation_history:
            if msg["content"] != user_input:
                role = "assistant" if msg["role"] == "tutor" else "user"
                messages.append({"role": role, "content": msg["content"]})

        messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                self.ollama_chat_api,
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_gpu": -1  # Force full GPU offloading
                        # Removed num_predict to allow natural, full-length answers
                    }
                },
                timeout=25
            )

            if response.status_code == 200:
                result = response.json()
                text = result.get('message', {}).get('content', '').strip()
                return text if text else "¿Puedes repetir?"

        except requests.exceptions.Timeout:
            return "Disculpa, intenta de nuevo. (Connection timed out)"
        except Exception as e:
            print(f"Ollama error: {e}")
            return "Error de conexión. (Connection error)"

        return "No entendí. (I didn't understand)"

    def send_message(self):
        user_input = self.input_text.get().strip()
        if not user_input:
            return

        if not self.ollama_available:
            messagebox.showerror("Error", "Ollama is not available")
            return

        self.input_text.delete(0, tk.END)
        self.add_message("Student", user_input, "user")

        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })

        # Check context length and warn user
        if len(self.conversation_history) == self.max_context_length:
            warning_msg = "⚠️ The conversation history is getting long. To prevent memory issues or slow responses, consider clearing the chat soon using the 'Clear' button."
            self.add_message("System", warning_msg, "warning")

        threading.Thread(target=self.process_response, args=(user_input,), daemon=True).start()

    def process_response(self, user_input):
        self.root.after(0, lambda: self.status_label.config(text="🤔 Thinking...", foreground="blue"))

        response = self.get_ollama_response(user_input)

        self.root.after(0, lambda: self.add_message("Tutor", response, "tutor"))

        self.conversation_history.append({
            "role": "tutor",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })

        if self.tts_enabled:
            threading.Thread(target=self.speak_text, args=(response,), daemon=True).start()

        self.root.after(0, lambda: self.status_label.config(text="🟢 Ready (Press F2 to speak)", foreground="green"))

    def speak_text(self, text):
        if not self.tts_enabled:
            return
        try:
            if PYTTSX3_AVAILABLE:
                engine.say(text)
                engine.runAndWait()
            else:
                commands = [
                    ["espeak-ng", "-v", "es", "-s", "120", text],
                    ["espeak", "-v", "es", "-s", "120", text]
                ]
                for cmd in commands:
                    try:
                        subprocess.run(cmd, capture_output=True, timeout=10, check=False)
                        break
                    except:
                        continue
        except Exception as e:
            print(f"TTS Error: {e}")

    def speak_last(self):
        for msg in reversed(self.conversation_history):
            if msg["role"] == "tutor":
                threading.Thread(target=self.speak_text, args=(msg["content"],), daemon=True).start()
                break

    def configure_tts(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Voice Configuration")
        dialog.geometry("300x200")
        tk.Label(dialog, text="TTS Settings", font=("Arial", 12, "bold")).pack(pady=10)

        if PYTTSX3_AVAILABLE:
            tk.Label(dialog, text="✅ pyttsx3 available", foreground="green").pack()
        else:
            tk.Label(dialog, text="⚠️ Using espeak", foreground="orange").pack()

        tk.Button(dialog, text="Test Voice", command=lambda: self.speak_text("Hola, probando la voz")).pack(pady=10)
        tk.Button(dialog, text="Close", command=dialog.destroy).pack()

    def save_conversation(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")],
            initialfile=f"spanish_lesson_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({"conversation": self.conversation_history}, f, ensure_ascii=False, indent=2)
            self.add_message("System", "Conversation saved", "system")

    def load_conversation(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.clear_conversation(confirm=False)
            self.conversation_history = data.get("conversation", [])
            for msg in self.conversation_history:
                role_label = "Student" if msg["role"] == "user" else "Tutor"
                self.add_message(role_label, msg["content"], msg["role"])
            self.add_message("System", "Conversation loaded", "system")

    def clear_conversation(self, confirm=True):
        if confirm and self.conversation_history:
            if not messagebox.askyesno("Confirm", "Clear conversation?"):
                return
        self.conversation_history.clear()
        self.conversation_text.config(state=tk.NORMAL)
        self.conversation_text.delete(1.0, tk.END)
        self.conversation_text.config(state=tk.DISABLED)
        if confirm:
            self.send_welcome()

    def show_stats(self):
        total = len(self.conversation_history)
        messagebox.showinfo("Statistics", f"Total messages: {total}")


def main():
    root = tk.Tk()
    app = ImprovedSpanishTutor(root)
    root.mainloop()


if __name__ == "__main__":
    main()