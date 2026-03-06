#!/usr/bin/env python3
"""
Quick Voice Parameter Playground
Test different voice settings quickly
"""

import subprocess
import sys

def test_voice(speed=120, pitch=50, gap=10, voice="spanish-latin-am", text=None):
    """Test espeak with given parameters"""
    if text is None:
        text = "Hola, ¿cómo estás? Me llamo tutor."
    
    cmd = [
        "espeak",
        "-v", voice,
        "-s", str(speed),
        "-p", str(pitch),
        "-g", str(gap),
        text
    ]
    
    print(f"🔊 Voice: {voice}, Speed: {speed}, Pitch: {pitch}, Gap: {gap}")
    print(f"   Text: '{text}'")
    
    try:
        subprocess.run(cmd, capture_output=True, timeout=10)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def quick_comparison():
    """Quick comparison of different settings"""
    print("\n🎯 Quick Voice Comparison")
    print("="*50)
    
    settings = [
        ("🐌 Very Slow & Clear", 90, 50, 20),
        ("📚 Learning Mode", 110, 50, 15),
        ("✅ Recommended", 120, 50, 10),
        ("🏃 Natural Speed", 140, 45, 8),
        ("⚡ Fast Native", 160, 45, 5),
    ]
    
    test_text = "Buenos días. ¿Cómo te llamas?"
    
    for name, speed, pitch, gap in settings:
        print(f"\n{name}:")
        test_voice(speed, pitch, gap, text=test_text)
        input("Press Enter for next...")

def voice_showcase():
    """Showcase different voice types"""
    print("\n🗣️ Voice Type Showcase")
    print("="*50)
    
    voices = [
        ("spanish", "Standard Spanish"),
        ("spanish-latin-am", "Latin American"),
        ("es", "Spanish Alternative"),
        ("es+f1", "Female Voice 1"),
        ("es+f3", "Female Voice 3"),
        ("es+m1", "Male Voice 1"),
    ]
    
    test_text = "Hola, soy tu tutor de español."
    
    for voice_code, voice_name in voices:
        print(f"\n{voice_name} ({voice_code}):")
        test_voice(voice=voice_code, text=test_text)
        input("Press Enter for next...")

def interactive_mode():
    """Interactive parameter adjustment"""
    print("\n🎛️ Interactive Voice Tuner")
    print("="*50)
    
    # Current settings
    settings = {
        "speed": 120,
        "pitch": 50,
        "gap": 10,
        "voice": "spanish-latin-am"
    }
    
    while True:
        print(f"\nCurrent: Speed={settings['speed']}, Pitch={settings['pitch']}, Gap={settings['gap']}")
        print("Commands:")
        print("  s100  - Set speed to 100")
        print("  p60   - Set pitch to 60")
        print("  g15   - Set gap to 15")
        print("  test  - Test current settings")
        print("  text  - Enter custom text")
        print("  quit  - Exit")
        
        cmd = input("\nCommand: ").strip().lower()
        
        if cmd.startswith('s'):
            try:
                settings['speed'] = int(cmd[1:])
                test_voice(**settings)
            except:
                print("❌ Invalid speed")
        
        elif cmd.startswith('p'):
            try:
                settings['pitch'] = int(cmd[1:])
                test_voice(**settings)
            except:
                print("❌ Invalid pitch")
        
        elif cmd.startswith('g'):
            try:
                settings['gap'] = int(cmd[1:])
                test_voice(**settings)
            except:
                print("❌ Invalid gap")
        
        elif cmd == 'test':
            test_voice(**settings)
        
        elif cmd == 'text':
            custom_text = input("Enter Spanish text: ")
            test_voice(**settings, text=custom_text)
        
        elif cmd == 'quit':
            break
        
        else:
            print("❌ Unknown command")

def main():
    print("╔══════════════════════════════════════════╗")
    print("║    🎤 Voice Parameter Playground 🎤      ║")
    print("╚══════════════════════════════════════════╝")
    
    while True:
        print("\n📋 Menu:")
        print("  1) Quick Comparison (hear different speeds)")
        print("  2) Voice Showcase (different voice types)")
        print("  3) Interactive Tuner (adjust parameters)")
        print("  4) Best Settings (recommended)")
        print("  5) Exit")
        
        choice = input("\nChoice [1-5]: ").strip()
        
        if choice == '1':
            quick_comparison()
        
        elif choice == '2':
            voice_showcase()
        
        elif choice == '3':
            interactive_mode()
        
        elif choice == '4':
            print("\n✨ Best Settings for Spanish Learning:")
            print("="*50)
            print("\n1️⃣ CLEAREST (Beginners):")
            print("   espeak -v spanish-latin-am -s 100 -p 50 -g 15")
            test_voice(100, 50, 15)
            
            print("\n2️⃣ BALANCED (Intermediate):")
            print("   espeak -v spanish-latin-am -s 120 -p 50 -g 10")
            test_voice(120, 50, 10)
            
            print("\n3️⃣ NATURAL (Advanced):")
            print("   espeak -v spanish-latin-am -s 140 -p 45 -g 5")
            test_voice(140, 45, 5)
            
            print("\n💡 TIP: Lower speed = clearer pronunciation!")
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            print("👋 Adiós!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Quick test mode
        if sys.argv[1] == '--slow':
            test_voice(100, 50, 15)
        elif sys.argv[1] == '--normal':
            test_voice(120, 50, 10)
        elif sys.argv[1] == '--fast':
            test_voice(140, 45, 5)
        else:
            # Custom parameters: voice_playground.py speed pitch gap
            try:
                speed = int(sys.argv[1])
                pitch = int(sys.argv[2]) if len(sys.argv) > 2 else 50
                gap = int(sys.argv[3]) if len(sys.argv) > 3 else 10
                test_voice(speed, pitch, gap)
            except:
                print("Usage: voice_playground.py [--slow|--normal|--fast]")
                print("   or: voice_playground.py speed [pitch] [gap]")
    else:
        main()
