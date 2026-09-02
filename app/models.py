from datetime import datetime, timezone
from app.extensions import db

class Repository(db.Model):
    __tablename__ = "repositories"

    id = db.Column(db.Integer, primary_key=True)
    github_rep_id = db.Column(db.BigInteger, unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    upstream_full_name = db.Column(db.String(255), nullable=True)
    default_branch = db.Column(db.String(100), nullable=False, default="main")
    created_at = db.Column(
        db.DateTime(timezone=True),
        default = lambda: datetime.now(timezone.utc),
        nullable=False,
    )