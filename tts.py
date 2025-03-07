from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

def process_tts(text, mode, language):
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            name="en-US-Wavenet-D" if language == "en-US" and mode == "friend" else 
                 "en-US-Wavenet-F" if language == "en-US" else 
                 "hi-IN-Wavenet-A" if mode == "friend" else "hi-IN-Wavenet-B"
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.9 if mode == "therapist" else 1.0,
            volume_gain_db=-3.0
        )
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        return response.audio_content
    except Exception as e:
        return b"Error synthesizing speech: " + str(e).encode()