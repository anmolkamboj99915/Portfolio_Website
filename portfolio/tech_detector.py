import requests
import os

TECH_FILE_MAP = {
    "requirements.txt": ["Python"],
    "Pipfile": ["Python"],
    "pyproject.toml": ["Python"],
    "package.json": ["Node.js", "JavaScript"],
    "Dockerfile": ["Docker"],
    "docker-compose.yml": ["Docker"],
}

def detect_technologies(repo_name):
    
    username = os.environ.get("GITHUB_USERNAME")
    token = os.environ.get("GITHUB_TOKEN")
    
    if not username:
        return []
    
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
    
    headers = {}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    try:
        response = requests.get(url, headers=headers)
    except requests.RequestException:
        return []
    
    if response.status_code != 200:
        return []
    
    try:
        files = response.json()
    except ValueError:
        return []
    
    if not isinstance(files, list):
        return []
    
    detected = set()
    
    for file in files:
        if not isinstance(file, dict):
            continue
        
        name = file.get("name")
        
        if name in TECH_FILE_MAP:
            
            for tech in TECH_FILE_MAP[name]:
                detected.add(tech)
    
    return list(detected)