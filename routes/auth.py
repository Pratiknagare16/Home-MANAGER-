"""Auth routes: login (email), signup, create home, forgot password stub, logout."""
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user
from extensions import db
from models.user import User
from models.home import Home
from models.user import ROLE_OWNER

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("signup.html")
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
            return render_template("signup.html")
        user = User(name=name or email, email=email)
        user.set_password(password)
        user.role = ROLE_OWNER
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created. Create your home below.", "success")
        return redirect(url_for("auth.create_home"))
    return render_template("signup.html")


@auth_bp.route("/create-home", methods=["GET", "POST"])
def create_home():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    if current_user.home_id:
        return redirect(url_for("dashboard.dashboard"))
    if request.method == "POST":
        home_name = request.form.get("home_name", "").strip() or "My Home"
        home = Home(home_name=home_name, owner_id=current_user.id)
        db.session.add(home)
        db.session.flush()
        current_user.home_id = home.id
        current_user.role = ROLE_OWNER
        db.session.commit()
        flash("Home created. You can invite members later.", "success")
        return redirect(url_for("dashboard.dashboard"))
    return render_template("create_home.html")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            # TODO: send reset link via Flask-Mail; for now show message
            flash("If an account exists for this email, you will receive a password reset link.", "info")
        else:
            flash("If an account exists for this email, you will receive a password reset link.", "info")
        return redirect(url_for("auth.login"))
    return render_template("forgot_password.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
