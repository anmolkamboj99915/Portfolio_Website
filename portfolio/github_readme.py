import requests
import os 
import base64
import re
from urllib.parse import quote


def fetch_readme(repo_name):
    
    if not repo_name:
        return None
    
    username = os.environ.get("GITHUB_USERNAME")
    token = os.environ.get("GITHUB_TOKEN")
    
    if not username:
        return None
    
    repo_name = quote(repo_name, safe="")
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    
    headers = {"Accept": "application/vnd.github+json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException:
        return None
    
    if response.status_code != 200:
        return None
    
    try:
        data = response.json()
    except ValueError:
        return None
    
    content = data.get("content")
    
    if data.get("encoding") != "base64":
        return None
    
    if not content:
        return None
    
    try:
        decoded = base64.b64decode(content.replace("\n", "")).decode("utf-8", errors="ignore")
    except Exception:
        return None
    
    return decoded

def clean_readme(text):
    
    if not text:
        return ""
    
    # remove images
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    
    # remove fenced code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    
    # remove inline code blocks
    text = re.sub(r"`[^`]*`", "", text)
    
    # remove links
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    
    # remove markdown symbols
    text = re.sub(r"[#>*]", "", text)
    
    # remove extra spaces
    text = re.sub(r"\n+", "\n", text)
    
    # limit text length
    summary = text.strip().split("\n")[0:5]
    
    return " ".join(summary)[:500]

