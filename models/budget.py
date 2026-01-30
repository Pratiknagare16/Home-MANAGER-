"""Budget – monthly limit per category; alerts when exceeded."""
from extensions import db


class Budget(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    home_id = db.Column(db.Integer, db.ForeignKey("homes.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("expense_categories.id"), nullable=True)  # null = total
    month_year = db.Column(db.String(7), nullable=False)  # "2025-01"
    limit_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
