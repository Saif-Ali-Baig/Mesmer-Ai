from models import db, Session, User

def log_session(user_id, input_text, response_text):
    session = Session(user_id=user_id, history={"input": input_text, "response": response_text})
    db.add(session)
    db.commit()

def update_user_prefs(user_id, prefs):
    user = User.get(User.id == user_id)
    if user:
        user.preferences = json.dumps({**json.loads(user.preferences or '{}'), **prefs})
        db.commit()
        return True
    return False

import json