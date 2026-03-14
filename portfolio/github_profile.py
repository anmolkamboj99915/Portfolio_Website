import requests
import os
from django.core.cache import cache


def fetch_github_profile():

    cached_profile = cache.get("github_profile")

    if cached_profile is not None:
        return cached_profile

    username = os.environ.get("GITHUB_USERNAME")
    token = os.environ.get("GITHUB_TOKEN")

    if not username:
        return None

    url = f"https://api.github.com/users/{username}"

    headers = {"Accept": "application/vnd.github+json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException:
        cache.set("github_profile", None, 300)
        return None

    if response.status_code != 200:
        cache.set("github_profile", None, 300)
        return None

    try:
        data = response.json()
    except ValueError:
        cache.set("github_profile", None, 300)
        return None


    profile = {
        "avatar": data.get("avatar_url"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "public_repos": data.get("public_repos"),
        "bio": data.get("bio"),
        "profile_url": data.get("html_url"),
    }

    cache.set("github_profile", profile, 3600)

    return profile
