from datetime import datetime, timezone
from app.extensions import db

class UpstreamChange(db.Model):
    __tablename__ = "upstream_changes"

    id = db.Column(db.Integer, primary_key=True)

    upstream_event_id = db.Column(
        db.Integer,
        db.ForeignKey("upstream_events.id"),
        nullable=False,
    )

    file_path = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    additions = db.Column(db.Integer, nullable=False, default=0)
    deletions = db.Column(db.Integer, nullable=False, default=0)
    changes = db.Column(db.Integer, nullable=False, default=0)

    event = db.relationship(
        "UpstreamEvent",
        back_populates="changes",
    )

class Repository(db.Model):
    __tablename__ = "repositories"

    id = db.Column(db.Integer, primary_key=True)
    github_repo_id = db.Column(
        db.BigInteger,
        unique=True,
        nullable=False,
    )

    full_name = db.Column(
        db.String(255),
        nullable=False,
    )

    upstream_full_name = db.Column(
        db.String(255),
        nullable=True,
    )

    default_branch = db.Column(
        db.String(100),
        nullable=False,
        default="main",
    )

    is_fork = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    baseline_sha = db.Column(
        db.String(40),
        nullable=True,
    )

    monitoring_enabled = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    upstream_events = db.relationship(
        "UpstreamEvent",
        back_populates="repository",
        cascade="all, delete-orphan",
    )

class UpstreamEvent(db.Model):
    __tablename__ = "upstream_events"
    id = db.Column(db.Integer, primary_key=True)
    repository_id = db.Column(
        db.Integer,
        db.ForeignKey("repositories.id"),
        nullable=False,
    )
    previous_sha = db.Column(
        db.String(40),
        nullable=False,
    )
    current_sha = db.Column(
        db.String(40),
        nullable=False,
    )
    detected_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    repository = db.relationship(
        "Repository",
        back_populates="upstream_events",
    )
    
    changes = db.relationship(
        "UpstreamChange",
        back_populates="event",
        cascade="all, delete-orphan",
    )