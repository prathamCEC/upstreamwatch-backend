from app.extensions import db
from app.models import Repository
from app.services.github_service import get_repository


def monitor_repository(full_name):
    github_repository = get_repository(full_name)

    existing_repository = Repository.query.filter_by(
        github_repo_id=github_repository.id
    ).first()

    if existing_repository:
        return None

    default_branch = github_repository.default_branch
    branch = github_repository.get_branch(default_branch)
    baseline_sha = branch.commit.sha

    upstream_full_name = (
        github_repository.parent.full_name
        if github_repository.fork and github_repository.parent
        else None
    )

    repository = Repository(
        github_repo_id=github_repository.id,
        full_name=github_repository.full_name,
        upstream_full_name=upstream_full_name,
        default_branch=default_branch,
        is_fork=github_repository.fork,
        baseline_sha=baseline_sha,
        monitoring_enabled=True,
    )

    db.session.add(repository)
    db.session.commit()

    return repository