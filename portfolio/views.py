from django.shortcuts import render, get_object_or_404
from .models import Project, Skill, Category

# Create your views here.
def index(request):
    
    category_id = request.GET.get("category")
    
    if category_id:
        projects = Project.objects.filter(category_id=category_id)
    else:
        projects = Project.objects.all()
        
    skills = Skill.objects.all()
    categories = Category.objects.all()
    
    return render(request, "portfolio/index.html", {
        "projects": projects,
        "skills": skills,
        "categories": categories,
    })
    
def project_detail(request, slug):
    
    project = get_object_or_404(Project, slug=slug)
    
    return render(request, "portfolio/project_detail.html", {
        "project": project
    })
