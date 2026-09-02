import asyncio
import os
import sys

async def _generate_and_play(text, language='en'):
    try:
        import edge_tts
    except ImportError:
        print("\n[AUDIO FAILSAFE]: 'edge-tts' is not installed.")
        print("To enable high-quality Edge audio, please run: pip install edge-tts")
        return False

    output_file = "radio_report.mp3"
    
    if language == 'hi':
        # Madhur is an excellent male Hindi/Hinglish neural voice
        voice = "hi-IN-MadhurNeural"
    else:
        # Christopher is a great, clear, energetic male voice for English. 
        voice = "en-US-ChristopherNeural" 
    
    print(f"INFO: Generating high-quality audio with Edge TTS ({voice})...")
    try:
        # Rate +10% gives it a slightly faster, radio-like pacing
        communicate = edge_tts.Communicate(text, voice, rate="+10%")
        await communicate.save(output_file)
        
        print(f"\n🎙️ Broadcasting report (via Edge TTS)...\n")
        
        # Cross-platform way to play the generated MP3
        if os.name == 'nt':  # Windows
            # startfile plays it in the background default player
            os.startfile(output_file)
            print("✅ Audio is playing in your default media player.")
        else:
            # Mac/Linux fallbacks
            if sys.platform == "darwin":
                os.system(f"afplay {output_file}")
            else:
                os.system(f"mpg123 {output_file} || play {output_file}")
                
        return True
    except Exception as e:
         print(f"\n[AUDIO FAILSAFE]: edge-tts encountered an error: {e}")
         return False

def speak_text_edge(text, language='en'):
    """
    Wrapper to run the async edge-tts code synchronously.
    """
    asyncio.run(_generate_and_play(text, language))
