"""Scope helpers: expenses/tasks for current user (home or personal)."""
from flask_login import current_user


def expense_scope():
    """Query base for expenses visible to current user."""
    from models.expense import Expense
    if current_user.home_id:
        return Expense.query.filter_by(home_id=current_user.home_id)
    return Expense.query.filter_by(user_id=current_user.id)


def task_scope():
    """Query base for tasks visible to current user."""
    from models.task import Task
    if current_user.home_id:
        from sqlalchemy import or_
        return Task.query.filter(
            or_(Task.home_id == current_user.home_id, Task.user_id == current_user.id)
        )
    return Task.query.filter_by(user_id=current_user.id)


def note_scope():
    """Query base for notes (always personal for now)."""
    from models.note import Note
    return Note.query.filter_by(user_id=current_user.id)
