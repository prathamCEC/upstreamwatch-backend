from flask import Blueprint, jsonify, request
from github import GithubException
from app.models import Repository
from app.services.repository_service import monitor_repository
from app.extensions import db

repositories_bp = Blueprint(
    "repositories",
    __name__,
    url_prefix="/api/repositories",
)


@repositories_bp.post("")
def create_repository_monitor():
    data = request.get_json()

    if not data or "full_name" not in data:
        return jsonify({
            "error": "full_name is required",
        }), 400
        
    try:
        repository = monitor_repository(data["full_name"])

        if repository is None:
            return jsonify({
                "error": "Repository is already being monitored",
            }), 409

        return jsonify({
            "repository": {
                "id": repository.id,
                "github_repo_id": repository.github_repo_id,
                "full_name": repository.full_name,
                "upstream_full_name": repository.upstream_full_name,
                "default_branch": repository.default_branch,
                "is_fork": repository.is_fork,
                "baseline_sha": repository.baseline_sha,
                "monitoring_enabled": repository.monitoring_enabled,
            }
        }), 201

    except GithubException as error:
        return jsonify({
            "error": "Unable to access repository on GitHub",
            "github_status": error.status,
        }), 502

@repositories_bp.get("")
def get_monitored_repositories():
    repositories = Repository.query.filter_by(
        monitoring_enabled=True
    ).all()
    return jsonify({
        "repositories": [
            {
                "id": repository.id,
                "github_repo_id": repository.github_repo_id,
                "full_name": repository.full_name,
                "upstream_full_name": repository.upstream_full_name,
                "default_branch": repository.default_branch,
                "is_fork": repository.is_fork,
                "baseline_sha": repository.baseline_sha,
                "monitoring_enabled": repository.monitoring_enabled,
            }
            for repository in repositories
        ]
    }), 200

@repositories_bp.get("/<int:repository_id>")
def get_monitored_repository(repository_id):
    repository = db.session.get(Repository, repository_id)

    if repository is None:
        return jsonify({
            "error": "Repository not found",
        }), 404

    return jsonify({
        "repository": {
            "id": repository.id,
            "github_repo_id": repository.github_repo_id,
            "full_name": repository.full_name,
            "upstream_full_name": repository.upstream_full_name,
            "default_branch": repository.default_branch,
            "is_fork": repository.is_fork,
            "baseline_sha": repository.baseline_sha,
            "monitoring_enabled": repository.monitoring_enabled,
        }
    }), 200