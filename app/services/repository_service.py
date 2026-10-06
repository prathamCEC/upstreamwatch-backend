from app.extensions import db
from app.models import Repository, UpstreamEvent, UpstreamChange
from app.services.github_service import (get_repository, get_repository_branch_sha,compare_commits,)


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

def check_upstream(repository):
    upstream_full_name = repository.upstream_full_name

    if not upstream_full_name:
        return {
            "upstream_changed": False,
            "reason": "Repository has no upstream repository",
        }

    current_sha = get_repository_branch_sha(
        upstream_full_name,
        repository.default_branch,
    )

    return {
        "upstream_changed": current_sha != repository.baseline_sha,
        "baseline_sha": repository.baseline_sha,
        "current_sha": current_sha,
    }

def process_upstream_changes(repository):
    result = check_upstream(repository)

    if not result["upstream_changed"]:
        return None

    comparison = compare_commits(
        repository.upstream_full_name,
        result["baseline_sha"],
        result["current_sha"],
    )

    event = UpstreamEvent(
        repository_id=repository.id,
        previous_sha=result["baseline_sha"],
        current_sha=result["current_sha"],
    )

    db.session.add(event)

    for file in comparison.files:
        change = UpstreamChange(
            file_path=file.filename,
            status=file.status,
            additions=file.additions,
            deletions=file.deletions,
            changes=file.changes,
        )

        event.changes.append(change)

    repository.baseline_sha = result["current_sha"]

    db.session.commit()

    return {
        "event_id": event.id,
        "previous_sha": event.previous_sha,
        "current_sha": event.current_sha,
        "total_commits": comparison.total_commits,
        "files_changed": len(comparison.files),
    }