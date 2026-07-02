"""Idempotent seed script.

Creates the database schema (if missing) and the default admin account.
Never create the SQLite file manually — always run this script (or let the
app factory + migrations do it).

Usage: python seed.py
"""
from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import User  # noqa: E402
from app.utils.enums import RoleEnum  # noqa: E402
from app.utils.security import hash_password  # noqa: E402


def seed_admin(app):
    with app.app_context():
        db.create_all()

        admin_email = app.config["DEFAULT_ADMIN_EMAIL"]
        existing = User.query.filter_by(email=admin_email).first()
        if existing:
            print(f"Admin already exists: {admin_email}")
            return

        admin = User(
            name=app.config["DEFAULT_ADMIN_NAME"],
            email=admin_email,
            password_hash=hash_password(app.config["DEFAULT_ADMIN_PASSWORD"]),
            role=RoleEnum.ADMIN,
            is_active=True,
            is_blacklisted=False,
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Default admin created: {admin_email} / {app.config['DEFAULT_ADMIN_PASSWORD']}")


if __name__ == "__main__":
    seed_admin(create_app())
