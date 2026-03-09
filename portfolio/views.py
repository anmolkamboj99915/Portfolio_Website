from django.shortcuts import render, get_object_or_404
from .models import Project, Skill, Category, Contact
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def index(request):
    
    category_id = request.GET.get("category")
    
    if category_id:
        projects = Project.objects.filter(category_id=category_id)
    else:
        projects = Project.objects.all()
        
    skills = Skill.objects.all()
    categories = Category.objects.all()
    
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        Contact.objects.create(
            name=name,
            email=email,
            message=message,
        )
        
        send_mail(
            subject=f"New Portfolio Message from {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
        )
        
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
