from peewee import *
from datetime import datetime

db = SqliteDatabase('voice_companion.db')  # Changed to Sqlite for simplicity, revert to Postgres if needed

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True)
    preferences = TextField(default='{}')

class Session(BaseModel):
    id = AutoField()
    user_id = IntegerField()
    history = TextField()
    created_at = DateTimeField(default=datetime.now)

def initialize_db():
    db.connect()
    db.create_tables([User, Session])

if __name__ == "__main__":
    initialize_db()