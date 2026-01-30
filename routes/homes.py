"""Home management – create (in auth), invite, members, settings (owner)."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.home import Home
from models.user import User, ROLE_OWNER, ROLE_MEMBER, ROLE_GUEST
from utils.permissions import can_manage_settings

homes_bp = Blueprint("homes", __name__, url_prefix="/home")


@homes_bp.route("")
@login_required
def view():
    if not current_user.home_id:
        return redirect(url_for("auth.create_home"))
    home = Home.query.get_or_404(current_user.home_id)
    if not can_manage_settings(current_user):
        flash("Only the home owner can manage settings.", "warning")
        return redirect(url_for("dashboard.dashboard"))
    members = User.query.filter_by(home_id=home.id).all()
    return render_template("home_settings.html", home=home, members=members)


@homes_bp.route("/invite", methods=["GET", "POST"])
@login_required
def invite():
    if not current_user.home_id:
        return redirect(url_for("auth.create_home"))
    if not can_manage_settings(current_user):
        flash("Only the home owner can invite members.", "warning")
        return redirect(url_for("dashboard.dashboard"))
    home = Home.query.get_or_404(current_user.home_id)
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        role = request.form.get("role", ROLE_MEMBER)
        if role not in (ROLE_MEMBER, ROLE_GUEST):
            role = ROLE_MEMBER
        # TODO: send invite email with token/link; for now show placeholder
        flash(f"Invite to {email} as {role} will be sent when email is configured.", "info")
        return redirect(url_for("homes.view"))
    return render_template("home_invite.html", home=home)
