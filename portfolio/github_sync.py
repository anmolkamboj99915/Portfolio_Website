from .github_service import fetch_github_projects
from .models import Project, Technology
from .github_readme import fetch_readme, clean_readme
from .tech_detector import detect_technologies
from datetime import datetime
import re
from .tag_detector import detect_project_tags
from django.utils import timezone


def generate_summary(text):
    if not text:
        return ""
    
    words = text.split()
    return " ".join(words[:40])

def detect_live_demo(text):
    if not text:
        return None
    patterns = [
        r"https://[a-zA-Z0-9\-]+\.vercel\.app",
        r"https://[a-zA-Z0-9\-]+\.netlify\.app",
        r"https://[a-zA-Z0-9\-]+\.onrender\.com",
        r"https://[a-zA-Z0-9\-]+\.railway\.app",
        r"https://[a-zA-Z0-9\-]+\.github\.io/[a-zA-Z0-9\-]+",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return None
    
    
def sync_github_projects():
    repos = fetch_github_projects() or []
    for repo in repos:
        
        if not isinstance(repo, dict):
            continue
        
        github_link = repo.get("github")
        repo_name = repo.get("name")
        
        if not github_link or not repo_name:
            continue
        
        description = str(repo.get("description") or "")
        live_link = repo.get("live")
        
        # If description is smal -> fetch README
        if not description or len(description) < 30:
            readme = fetch_readme(repo_name)
            
            if readme:
                description = str(clean_readme(readme) or "")
            
                live_demo = detect_live_demo(readme)
                if live_demo:
                    live_link = live_demo
                
        project, created = Project.objects.get_or_create(
            github_link = github_link,
            defaults={
                "title": repo.get("name") or "Unnamed Project",
                "description": generate_summary(description),
                "live_link": live_link,
                "is_github_project": True,
                "github_stars": repo.get("stars", 0),
                "github_forks": repo.get("forks", 0),
                "github_size": repo.get("size", 0),
            },
        )
        
        if not created:
            project.description = generate_summary(description)
            project.live_link = live_link
            project.github_stars = repo.get("stars", 0)
            project.github_forks = repo.get("forks", 0)
            project.github_size = repo.get("size", 0)
            project.github_watchers = repo.get("watchers", 0)
            project.github_issues = repo.get("issues", 0)
            
            if repo.get("updated"):
                try:
                    dt = datetime.strptime(repo["updated"], "%Y-%m-%dT%H:%M:%SZ")
                    project.github_last_updated = timezone.make_aware(dt)
                except Exception:
                    pass
                
            project.save()
        
        detected_techs = []
        for tech in detect_technologies(description) or []:
            tech = str(tech).strip().lower()
            if tech and tech not in detected_techs:
                detected_techs.append(tech)        
        
        language = (repo.get("language") or "").strip().lower()
        detected_lower = detected_techs
        if language and language not in detected_lower:
            detected_techs.append(language)
            
        existing_tech_ids = set(
            project.technologies.values_list("id", flat=True)
        )
        
        for tech_name in detected_techs:
            tech_name = str(tech_name).strip().lower()
            
            if not tech_name:
                continue
            
            tech, _ = Technology.objects.get_or_create(
                name=tech_name
            )
            
            if tech.id not in existing_tech_ids:
                project.technologies.add(tech)
                existing_tech_ids.add(tech.id)
                
        # Recalculate tech names after updates
        tech_names = [name.lower() for name in project.technologies.values_list("name", flat=True)]
    
        tags = detect_project_tags(
            project.title or "",
            project.description or "",
            tech_names,
        )
        if project.tags != tags:
            project.tags = tags
            project.save(update_fields=["tags"])
                    
