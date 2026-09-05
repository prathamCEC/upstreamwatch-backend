from flask import Blueprint, jsonify
from app.services.github_service import get_installation_repositories

github_bp = Blueprint("github", __name__, url_prefix="/api/github")

@github_bp.get("/repositories")
def get_repositories():
    try:
        repositories = get_installation_repositories()
        return jsonify({
            "repositories": repositories,
        }),200
    except GithubException as error:
        return jsonify({
            "error": "Failed to retrieve repositories from GitHub",
            "github_status": error.status,
        }),502