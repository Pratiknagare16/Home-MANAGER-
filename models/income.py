"""Income tracking – salary, side income, shared household."""
from extensions import db
from datetime import date


class Income(db.Model):
    __tablename__ = "incomes"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey("homes.id"), nullable=True)
    date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=db.func.now())
