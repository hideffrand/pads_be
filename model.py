from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Note(db.Model):
    __tablename__ = "pads_note"

    note_id = db.Column('note_id', db.Integer, primary_key=True)
    note_title = db.Column('note_title', db.Text, nullable=False)
    note_description = db.Column('note_description', db.Text, nullable=False)
    note_type = db.Column('note_type', db.String(10), nullable=False)
    # ^ important, urgent, reguler, don
    created_at = db.Column('created_at', db.DateTime, nullable=False)

    def __init__(self, note_id, note_title, note_description, note_type, created_at):
        self.note_id = note_id
        self.note_title = note_title
        self.note_description = note_description
        self.note_type = note_type
        self.created_at = created_at

    def to_json(self):
        return {
            "note_id": self.note_id,
            "note_title": self.note_title,
            "note_description": self.note_description,
            "note_type": self.note_type,
            "created_at": self.created_at,
        }
