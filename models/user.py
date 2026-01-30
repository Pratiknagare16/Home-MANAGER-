"""User model – identity, role, home membership. Login by email."""
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Role: owner | member | guest
ROLE_OWNER = "owner"
ROLE_MEMBER = "member"
ROLE_GUEST = "guest"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="")
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default=ROLE_OWNER)  # owner | member | guest
    home_id = db.Column(db.Integer, db.ForeignKey("homes.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Backref: user.home (Home or None)
    home = db.relationship("Home", backref="members", foreign_keys=[home_id])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_owner(self):
        return self.role == ROLE_OWNER

    def is_member_or_owner(self):
        return self.role in (ROLE_OWNER, ROLE_MEMBER)

    @property
    def display_name(self):
        return self.name.strip() or self.email
