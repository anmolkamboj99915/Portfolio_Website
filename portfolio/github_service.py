import requests
import os


def fetch_github_projects():

    username = os.environ.get("GITHUB_USERNAME")
    token = os.environ.get("GITHUB_TOKEN")

    url = f"https://api.github.com/users/{username}/repos"

    headers = {}

    if token:
        headers["Authorization"] = f"token {token}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    repos = response.json()

    projects = []

    for repo in repos:
        if not repo["fork"]:
            projects.append({
                "name": repo["name"],
                "description": repo["description"] or "",
                "github": repo["html_url"],
                "live": None,
            })

    return projects