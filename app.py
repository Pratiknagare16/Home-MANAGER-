"""Home Manager – Flask app entry point."""
from flask import Flask
from extensions import db, login_manager

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."

# Import models in dependency order (user → home → categories → expense/task/note/income/budget)
import models.user  # noqa: E402, F401
import models.home  # noqa: E402, F401
import models.expense_category  # noqa: E402, F401
import models.expense  # noqa: E402, F401
import models.task  # noqa: E402, F401
import models.note  # noqa: E402, F401
import models.income  # noqa: E402, F401
import models.budget  # noqa: E402, F401

from routes.auth import auth_bp  # noqa: E402
from routes.dashboard import dashboard_bp  # noqa: E402
from routes.homes import homes_bp  # noqa: E402
from routes.expenses import expenses_bp  # noqa: E402
from routes.tasks import tasks_bp  # noqa: E402
from routes.notes import notes_bp  # noqa: E402

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(homes_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(notes_bp)


@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))


@app.route("/")
def index():
    from flask import redirect
    from flask_login import current_user
    if current_user.is_authenticated:
        return redirect("/dashboard")
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
