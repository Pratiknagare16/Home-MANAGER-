"""Note routes – list, add, edit, delete."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.note import Note

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


@notes_bp.route("", methods=["GET", "POST"])
@login_required
def list_notes():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if title:
            note = Note(title=title, content=content, user_id=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash("Note added.", "success")
        return redirect(url_for("notes.list_notes"))
    all_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.id.desc()).all()
    return render_template("notes.html", notes=all_notes)


@notes_bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        note.title = request.form.get("title", "").strip() or note.title
        note.content = request.form.get("content", "").strip()
        db.session.commit()
        flash("Note updated.", "success")
        return redirect(url_for("notes.list_notes"))
    return render_template("note_edit.html", note=note)


@notes_bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    flash("Note removed.", "success")
    return redirect(url_for("notes.list_notes"))
