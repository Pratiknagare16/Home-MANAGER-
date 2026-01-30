"""Task / chore – assign, due date, priority, status, repeating."""
from extensions import db
from datetime import date, datetime

# Status: todo | in_progress | done
STATUS_TODO = "todo"
STATUS_IN_PROGRESS = "in_progress"
STATUS_DONE = "done"
PRIORITY_LOW = "low"
PRIORITY_MEDIUM = "medium"
PRIORITY_HIGH = "high"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    assigned_to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), default=PRIORITY_MEDIUM)
    status = db.Column(db.String(20), default=STATUS_TODO)
    is_repeating = db.Column(db.Boolean, default=False)
    home_id = db.Column(db.Integer, db.ForeignKey("homes.id"), nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Legacy: task/completed/user_id for backward compat with existing templates
    task = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    @property
    def is_completed(self):
        return self.status == STATUS_DONE or self.completed

    def _get_display_title(self):
        return self.title or self.task or ""

    def _set_display_title(self, v):
        self.title = v
        self.task = v

    display_title = property(_get_display_title, _set_display_title)
