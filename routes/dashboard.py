"""Dashboard – single pane of glass: totals, pending tasks, quick add."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.expense import Expense
from models.task import Task
from models.note import Note
from models.budget import Budget
from utils.scope import expense_scope, task_scope, note_scope
from datetime import datetime, timedelta
from sqlalchemy import func
import json

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    if not current_user.home_id:
        return redirect(url_for("auth.create_home"))
        
    # Scopes
    expenses_q = expense_scope()
    tasks_q = task_scope()
    notes_q = note_scope()
    
    # 1. KPIs
    all_exp = expenses_q.all()
    total_expense_sum = sum(e.amount for e in all_exp)
    
    all_tasks = tasks_q.all()
    pending_tasks = sum(1 for t in all_tasks if not t.is_completed)
    
    notes_count = notes_q.count()
    
    # Budget Remaining (This Month)
    today = datetime.today()
    current_month_str = today.strftime("%Y-%m")
    
    # Get total budget for this month
    budget = Budget.query.filter_by(
        home_id=current_user.home_id, 
        month_year=current_month_str, 
        category_id=None
    ).first()
    
    budget_limit = budget.limit_amount if budget else 0
    
    # Calculate expenses for this month
    this_month_expenses = sum(
        e.amount for e in all_exp 
        if e.date.strftime("%Y-%m") == current_month_str
    )
    
    budget_remaining = budget_limit - this_month_expenses if budget_limit > 0 else 0
    
    # 2. Charts Data
    # Category Breakdown
    category_data = {}
    for e in all_exp:
        cat_name = e.category.name if e.category else "Uncategorized"
        category_data[cat_name] = category_data.get(cat_name, 0) + e.amount
    
    chart_category_labels = list(category_data.keys())
    chart_category_values = list(category_data.values())
    
    # Monthly Trend (Last 6 months)
    monthly_data = {}
    for i in range(5, -1, -1):
        d = today - timedelta(days=i*30) # Approx
        m_str = d.strftime("%Y-%m")
        monthly_data[m_str] = 0
        
    for e in all_exp:
        m_str = e.date.strftime("%Y-%m")
        if m_str in monthly_data:
            monthly_data[m_str] += e.amount
            
    # Sort by month
    sorted_months = sorted(monthly_data.keys())
    chart_monthly_labels = [datetime.strptime(m, "%Y-%m").strftime("%b") for m in sorted_months]
    chart_monthly_values = [monthly_data[m] for m in sorted_months]

    # 3. Recent Items
    recent_expenses = list(expenses_q.order_by(Expense.date.desc(), Expense.id.desc()).limit(5).all())
    recent_tasks = list(tasks_q.order_by(Task.completed.asc(), Task.due_date.asc(), Task.id.desc()).limit(5).all())

    return render_template(
        "dashboard.html",
        total_expense=total_expense_sum,
        pending_tasks=pending_tasks,
        notes_count=notes_count,
        budget_remaining=budget_remaining,
        has_budget=(budget_limit > 0),
        recent_expenses=recent_expenses,
        recent_tasks=recent_tasks,
        home=current_user.home,
        chart_category_labels=json.dumps(chart_category_labels),
        chart_category_values=json.dumps(chart_category_values),
        chart_monthly_labels=json.dumps(chart_monthly_labels),
        chart_monthly_values=json.dumps(chart_monthly_values),
    )