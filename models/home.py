"""Home / household model – one home, many users; owner/member/guest."""
from extensions import db
from datetime import datetime


class Home(db.Model):
    __tablename__ = "homes"

    id = db.Column(db.Integer, primary_key=True)
    home_name = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship("User", foreign_keys=[owner_id])
    # Backref: home.members (list of User)
