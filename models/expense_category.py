"""Expense category – Food, Rent, Travel, etc. Per-home or default."""
from extensions import db


class ExpenseCategory(db.Model):
    __tablename__ = "expense_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey("homes.id"), nullable=True)  # null = default set
