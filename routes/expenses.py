"""Expense routes – list, add, delete. Home-scoped; permission-aware."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.expense import Expense
from models.expense_category import ExpenseCategory
from utils.scope import expense_scope
from utils.permissions import can_manage_expenses, can_view_expenses

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


def _default_categories():
    """Default categories when none exist (e.g. Food, Rent, Travel)."""
    if current_user.home_id:
        cats = ExpenseCategory.query.filter_by(home_id=current_user.home_id).all()
        if not cats:
            for name in ["Food", "Rent", "Travel", "Utilities", "Other"]:
                c = ExpenseCategory(name=name, home_id=current_user.home_id)
                db.session.add(c)
            db.session.commit()
            cats = ExpenseCategory.query.filter_by(home_id=current_user.home_id).all()
        return cats
    return []


@expenses_bp.route("", methods=["GET", "POST"])
@login_required
def list_expenses():
    if not current_user.home_id:
        return redirect(url_for("auth.create_home"))
    if request.method == "POST" and can_manage_expenses(current_user):
        title = request.form.get("title", "").strip()
        try:
            amount = float(request.form.get("amount", 0))
        except (TypeError, ValueError):
            amount = 0.0
        category_id = request.form.get("category_id") or None
        if category_id:
            try:
                category_id = int(category_id)
            except (TypeError, ValueError):
                category_id = None
        payment_method = request.form.get("payment_method", "other")
        if title:
            exp = Expense(
                title=title,
                amount=amount,
                category_id=category_id,
                payment_method=payment_method,
                paid_by_user_id=current_user.id,
                home_id=current_user.home_id,
                user_id=current_user.id,
            )
            db.session.add(exp)
            db.session.commit()
            flash("Expense added.", "success")
        return redirect(url_for("expenses.list_expenses"))
    all_expenses = expense_scope().order_by(Expense.id.desc()).all()
    total = sum(e.amount for e in all_expenses)
    categories = _default_categories()
    return render_template(
        "expenses.html",
        expenses=all_expenses,
        total=total,
        categories=categories,
        can_edit=can_manage_expenses(current_user),
    )


@expenses_bp.route("/<int:expense_id>/delete", methods=["POST"])
@login_required
def delete_expense(expense_id):
    if not can_manage_expenses(current_user):
        flash("You cannot delete expenses.", "danger")
        return redirect(url_for("expenses.list_expenses"))
    exp = expense_scope().filter_by(id=expense_id).first_or_404()
    db.session.delete(exp)
    db.session.commit()
    flash("Expense removed.", "success")
    return redirect(url_for("expenses.list_expenses"))
