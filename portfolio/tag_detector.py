def detect_project_tags(name, description, technologies):
    tags = []
    text = f" {name or ''} {description or ''} ".lower()
    technologies = [str(t).lower() for t in (technologies or [])]
    if " ai " in text:
        tags.append("AI")
    
    if " api " in text:
        tags.append("API")
        
    if any(t in technologies for t in ["django", "flask", "fastapi"]):
        tags.append("Web App")
    
    if " cli " in text:
        tags.append("CLI Tool")
    
    if "machine learning" in text:
        tags.append("Machine Learning")
    
    if "automation" in text:
        tags.append("Automation")
    
    return list(dict.fromkeys(tags))
        