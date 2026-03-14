import requests
import os
from django.core.cache import cache


def fetch_github_projects():
    cached_projects = cache.get("github_projects")
    if cached_projects is not None:
        return cached_projects

    username = os.environ.get("GITHUB_USERNAME")
    token = os.environ.get("GITHUB_TOKEN")

    if not username:
        cache.set("github_projects", [], 300)
        return []

    url = f"https://api.github.com/users/{username}/repos?per_page=100"

    headers = {
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException:
        cache.set("github_projects", [], 300)
        return []

    if response.status_code != 200:
        cache.set("github_projects", [], 300)
        return []

    try:
        repos = response.json()
        if not isinstance(repos, list):
            cache.set("github_projects", [], 300)
            return []
    except ValueError:
        cache.set("github_projects", [], 300)
        return []

    projects = []

    for repo in repos:
        if repo.get("fork") or repo.get("private"):
            continue
        projects.append({
            "name": repo.get("name") or "Unnamed Project",
            "description": repo.get("description") or "",
            "github": repo.get("html_url"),
            "live": repo.get("homepage") or "",
            "language": repo.get("language"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("fork_count", 0),
            "watchers": repo.get("watchers_count", 0),
            "issues": repo.get("open_issues_count", 0),
            "size": repo.get("size", 0),
            "updated": repo.get("updated_at"),
        })
        
    cache.set("github_projects", projects, 3600)
    return projects