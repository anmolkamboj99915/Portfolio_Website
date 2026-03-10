from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Skill, Category, Contact, Visitor
from django.core.mail import send_mail
from django.conf import settings
from .github_service import fetch_github_projects
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Count
from django_ratelimit.decorators import ratelimit

# Create your views here.

@ratelimit(key="ip", rate="10/m", block=True)
def index(request):
    
    category_id = request.GET.get("category")
    
    if request.method == "GET":
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        
        today = timezone.now().date()

        Visitor.objects.create(
            ip_address=ip,
            page="home",
            created_at__date=today
        )

    projects = Project.objects.all().prefetch_related("technologies")
    if category_id:
        projects = projects.filter(category_id=category_id)
        
    search_query = request.GET.get("search")
    if search_query:
        projects = projects.filter(
            title__icontains=search_query
        )

    skills = Skill.objects.all()
    categories = Category.objects.all()
    
    github_projects = cache.get("github_projects")

    if github_projects is None:
        github_projects = fetch_github_projects()
        cache.set("github_projects", github_projects, 3600)


    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if name and email and message:
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
            return redirect("home")
        

    return render(request, "portfolio/index.html", {
        "projects": projects,
        "skills": skills,
        "categories": categories,
        "github_projects": github_projects,
    })
    
def project_detail(request, slug):
    
    project = get_object_or_404(Project, slug=slug)

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    Visitor.objects.create(
        ip_address=ip,
        page=f"project: {project.slug}"
    )
    
    return render(request, "portfolio/project_detail.html", {
        "project": project
    })


def analytics(request):

    total_visitors = Visitor.objects.count()
    total_projects = Project.objects.count()
    total_messages = Contact.objects.count()

    top_projects = (
        Visitor.objects.filter(page__startswith="project:").values("page").annotate(count=Count("id")).order_by("-count")[:5]
    )

    return render(request, "portfolio/analytics.html", {
        "total_visitors": total_visitors,
        "total_projects": total_projects,
        "total_messages": total_messages,
        "top_projects": top_projects,
    })
