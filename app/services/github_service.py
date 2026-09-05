import os
import time
import jwt
from github import Github, GithubIntegration
from github.Auth import AppAuth


def create_app_jwt():
    app_id = os.getenv("GITHUB_APP_ID")
    private_key_path = os.getenv("GITHUB_PRIVATE_KEY_PATH")

    with open(private_key_path, "r") as key_file:
        private_key = key_file.read()

    now = int(time.time())

    payload = {
        "iat": now,
        "exp": now + 600,
        "iss": app_id,
    }

    return jwt.encode(payload, private_key, algorithm="RS256")


def _get_github_integration():
    app_id = os.getenv("GITHUB_APP_ID")
    private_key_path = os.getenv("GITHUB_PRIVATE_KEY_PATH")

    with open(private_key_path, "r") as key_file:
        private_key = key_file.read()

    auth = AppAuth(
        app_id=app_id,
        private_key=private_key,
    )

    return GithubIntegration(auth=auth)


def create_installation_token():
    installation_id = int(os.getenv("GITHUB_INSTALLATION_ID"))
    integration = _get_github_integration()
    access_token = integration.get_access_token(installation_id)

    return access_token.token


def get_github_client():
    token = create_installation_token()
    return Github(token)


def get_installation_repositories():
    installation_id = int(os.getenv("GITHUB_INSTALLATION_ID"))
    integration = _get_github_integration()
    installation = integration.get_app_installation(installation_id)
    repositories = installation.get_repos()

    return [
        {
            "github_id": repository.id,
            "full_name": repository.full_name,
            "default_branch": repository.default_branch,
            "private": repository.private,
            "is_fork": repository.fork,
            "upstream_full_name": (
                repository.parent.full_name
                if repository.fork and repository.parent
                else None
            ),
        }
        for repository in repositories
    ]