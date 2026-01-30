"""Note model – manage notes."""
from extensions import db


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, default="")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
