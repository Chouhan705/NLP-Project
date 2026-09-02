def speak_text_pyttsx3(text, language='en'):
    """
    Initializes pyttsx3 and reads the text aloud.
    Includes failsafes if pyttsx3 is not installed or encounters an error.
    """
    try:
        import pyttsx3
    except ImportError:
        print("\n[AUDIO FAILSAFE]: 'pyttsx3' is not installed.")
        print("To enable offline audio, please run: pip install pyttsx3")
        return False
        
    try:
        print("INFO: Initializing pyttsx3 audio module...")
        engine = pyttsx3.init()
        
        if language == 'hi':
            # Try to find a Hindi voice (e.g., Kalpana on Windows)
            voices = engine.getProperty('voices')
            hindi_voice_found = False
            for voice in voices:
                if 'hin' in voice.id.lower() or 'hindi' in voice.name.lower() or 'kalpana' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    hindi_voice_found = True
                    print(f"INFO: Selected Hindi voice: {voice.name}")
                    break
            if not hindi_voice_found:
                print("WARNING: No native Hindi voice found. Using default voice (might sound weird).")
        
        # Radio Jockey styling: Make the voice slightly more energetic (faster rate)
        engine.setProperty('rate', 215)
        
        # Ensure max volume
        engine.setProperty('volume', 1.0)
        
        print("\n🎙️ Broadcasting report (via pyttsx3)...\n")
        engine.say(text)
        engine.runAndWait()
        print("\n✅ Broadcast complete!")
        return True
        
    except Exception as e:
        print(f"\n[AUDIO FAILSAFE]: pyttsx3 engine encountered an error: {e}")
        return False
