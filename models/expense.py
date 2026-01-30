"""Expense model – categories, payment method, paid by, split, recurring."""
from extensions import db
from datetime import date

# Payment methods (can be extended via table later)
PAYMENT_CASH = "cash"
PAYMENT_UPI = "upi"
PAYMENT_CARD = "card"
PAYMENT_OTHER = "other"


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("expense_categories.id"), nullable=True)
    payment_method = db.Column(db.String(20), default=PAYMENT_OTHER)
    paid_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    home_id = db.Column(db.Integer, db.ForeignKey("homes.id"), nullable=True)
    date = db.Column(db.Date, default=date.today)
    is_recurring = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Legacy: user_id for "added by" when no home
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    home = db.relationship("Home", backref="expenses")
    category = db.relationship("ExpenseCategory", backref="expenses")
    paid_by = db.relationship("User", foreign_keys=[paid_by_user_id])
    splits = db.relationship("ExpenseSplit", backref="expense", cascade="all, delete-orphan")


class ExpenseSplit(db.Model):
    """Split share per member for an expense."""
    __tablename__ = "expense_splits"

    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey("expenses.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    share_amount = db.Column(db.Float, nullable=False)
