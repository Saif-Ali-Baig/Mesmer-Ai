import sys
from stt import process_stt
from ai import process_ai
from tts import process_tts
from session import log_session, update_user_prefs
from models import db, User

db_url = 'postgresql://jace:password123@localhost:5432/voice_companion'
db.bind(provider='postgres', user='jace', password='password123', host='localhost', database='voice_companion')
db.generate_mapping(create_tables=True)

def main():
    mode = sys.argv[1]
    user_id = int(sys.argv[2])
    audio_bytes = sys.stdin.buffer.read()
    
    user = User.get(User.id == user_id)
    if not user:
        sys.stdout.buffer.write(b"Error: User not found")
        return
    
    text, detected_lang = process_stt(audio_bytes)
    if detected_lang is None:
        audio_response = process_tts("Try again, please?", mode, "en-US")
    else:
        if user.preferences.get('mode') != mode:
            update_user_prefs(user.id, {'mode': mode})
        response_text = process_ai(text, mode, user, detected_lang)
        audio_response = process_tts(response_text, mode, detected_lang)
        log_session(user.id, text, response_text)
    
    sys.stdout.buffer.write(audio_response)

if __name__ == "__main__":
    main()