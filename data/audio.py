import sys

def speak_text(text):
    """
    Initializes pyttsx3 and reads the text aloud.
    Includes failsafes if pyttsx3 is not installed or encounters an error.
    """
    try:
        import pyttsx3
    except ImportError:
        print("\n[AUDIO FAILSAFE]: 'pyttsx3' is not installed.")
        print("To enable audio, please run: pip install pyttsx3")
        print(f"\n[FALLBACK SCRIPT]\n{text}\n")
        return False
        
    try:
        print("INFO: Initializing audio module...")
        engine = pyttsx3.init()
        
        # Radio Jockey styling: Make the voice slightly more energetic (faster rate)
        # Default rate is often around 200 on Windows. 215 makes it sound upbeat.
        engine.setProperty('rate', 215)
        
        # Ensure max volume
        engine.setProperty('volume', 1.0)
        
        print("\n🎙️ Broadcasting report...\n")
        engine.say(text)
        engine.runAndWait()
        print("\n✅ Broadcast complete!")
        return True
        
    except Exception as e:
        print(f"\n[AUDIO FAILSAFE]: Audio engine encountered an error: {e}")
        print(f"\n[FALLBACK SCRIPT]\n{text}\n")
        return False
