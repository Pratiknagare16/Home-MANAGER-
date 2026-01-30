"""Task / chore routes – list, add, toggle, delete. Home-scoped; assign, priority, status."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.task import Task, STATUS_TODO, STATUS_DONE
from utils.scope import task_scope
from utils.permissions import can_manage_tasks

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET", "POST"])
@login_required
def list_tasks():
    if not current_user.home_id:
        return redirect(url_for("auth.create_home"))
    if request.method == "POST" and can_manage_tasks(current_user):
        task_title = request.form.get("task", "").strip()
        if task_title:
            t = Task(
                title=task_title,
                task=task_title,
                user_id=current_user.id,
                home_id=current_user.home_id,
                created_by_user_id=current_user.id,
                status=STATUS_TODO,
            )
            db.session.add(t)
            db.session.commit()
            flash("Task added.", "success")
        return redirect(url_for("tasks.list_tasks"))
    all_tasks = task_scope().order_by(Task.completed.asc(), Task.id.desc()).all()
    pending_count = sum(1 for t in all_tasks if not t.is_completed)
    from models.user import User
    members = User.query.filter_by(home_id=current_user.home_id).all() if current_user.home_id else []
    return render_template(
        "tasks.html",
        tasks=all_tasks,
        pending_count=pending_count,
        members=members,
        can_edit=can_manage_tasks(current_user),
    )


@tasks_bp.route("/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_task(task_id):
    t = task_scope().filter_by(id=task_id).first_or_404()
    if not can_manage_tasks(current_user):
        flash("You cannot change task status.", "warning")
        return redirect(url_for("tasks.list_tasks"))
    t.completed = not t.completed
    t.status = STATUS_DONE if t.completed else STATUS_TODO
    db.session.commit()
    return redirect(url_for("tasks.list_tasks"))


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    if not can_manage_tasks(current_user):
        flash("You cannot remove tasks.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    t = task_scope().filter_by(id=task_id).first_or_404()
    db.session.delete(t)
    db.session.commit()
    flash("Task removed.", "success")
    return redirect(url_for("tasks.list_tasks"))
