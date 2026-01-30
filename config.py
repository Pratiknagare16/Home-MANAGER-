"""App configuration. Use env vars in production."""
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecret-change-in-production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
