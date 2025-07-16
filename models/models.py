from datetime import datetime

from peewee import SqliteDatabase, Model, BigIntegerField, CharField, DateTimeField, TextField

db = SqliteDatabase("nox_feedback.db")


class BaseModel(Model):
    class Meta:
        database = db


class Review(BaseModel):
    user_id = BigIntegerField()
    table_size = CharField()
    feedback_status = CharField()
    feedback_text = TextField(null=True)
    timestamp = DateTimeField(default=datetime.now)


def create_tables():
    db.connect()
    db.create_tables([Review], safe=True)
    db.close()
