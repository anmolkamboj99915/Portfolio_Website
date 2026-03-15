from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Skill, Category, Contact, Visitor, Technology
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count
from django_ratelimit.decorators import ratelimit
from django.db.models import Sum
import markdown
from .github_readme import fetch_readme
from django.http import JsonResponse
from .github_profile import fetch_github_profile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .tasks import sync_github


# Create your views here.

@ratelimit(key="ip", rate="10/m", block=True)
def index(request):
    try:
        if not cache.get("github_synced") and cache.add("github_sync_running", True, 300):
            sync_github()
    except Exception:
        pass
    
    category_id = request.GET.get("category")
    
    if request.method == "GET":
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip() or "0.0.0.0"
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        
        Visitor.objects.create(
            ip_address=ip,
            page="home",
        )

    projects = (
        Project.objects.select_related("category")
        .prefetch_related("technologies")
        .order_by("-github_stars", "-github_last_updated", "-id")
    )
    
    tech_filter = request.GET.get("tech")
    
    if tech_filter:
        projects = projects.filter(technologies__name__icontains=tech_filter)
    
    if category_id:
        projects = projects.filter(category_id=category_id)
        
    search_query = request.GET.get("search")
    if search_query and search_query.strip():
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(technologies__name__icontains=search_query)
        ).distinct()

    skills = cache.get("skills")
    if skills is None:
        skills = list(Skill.objects.all())
        try:    
            cache.set("skills", skills, 3600)
        except Exception:
            pass
        
    categories = cache.get("categories")
    if categories is None:
        categories = list(Category.objects.all())
        try:
            cache.set("categories", categories, 3600)
        except Exception:
            pass
        
    github_project_ids = cache.get("github_project_ids")

    if github_project_ids is None:
        
        github_project_ids = list(
            Project.objects.filter(is_github_project=True).values_list("id", flat=True)
        )
        try:
            cache.set("github_project_ids", github_project_ids, 3600)
        except Exception:
            pass
        
    github_projects = Project.objects.filter(id__in=github_project_ids).order_by(
        "-github_stars", "-github_last_updated"
    )

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

            try:
                send_mail(
                    subject=f"New Portfolio Message from {name}",
                    message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                )
            except Exception:
                pass

            return redirect("home")
        
    github_profile = cache.get("github_profile")
    if github_profile is None:    
        github_profile = fetch_github_profile()
        try:
            cache.set("github_profile", github_profile, 3600)
        except Exception:
            pass
        
    technologies = cache.get("technologies")
    if technologies is None:
        technologies = list(Technology.objects.values_list("id", flat=True))
        try:
            cache.set("technologies", technologies, 3600)
        except Exception:
            pass
        
    technologies = Technology.objects.filter(id__in=technologies)
    
    return render(request, "portfolio/index.html", {
        "projects": projects,
        "skills": skills,
        "categories": categories,
        "github_projects": github_projects,
        "github_profile": github_profile,
        "technologies": technologies,
    })
    
def project_detail(request, slug):
    
    project = get_object_or_404(Project, slug=slug)

    readme_html = None
    
    if project.github_link:
        repo_name = project.github_link.rstrip("/").split("/")[-1]
        readme = fetch_readme(repo_name)
        
        if readme: 
            readme_html = markdown.markdown(readme, extensions=["fenced_code", "tables"])
            
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip() or "0.0.0.0"
    else:
        ip = request.META.get("REMOTE_ADDR", "0.0.0.0")

    Visitor.objects.create(
        ip_address=ip,
        page=f"project: {project.slug}"
    )
    
    return render(request, "portfolio/project_detail.html", {
        "project": project,
        "readme_html": readme_html,
    })


def analytics(request):

    total_visitors = Visitor.objects.count()
    total_projects = Project.objects.count()
    total_messages = Contact.objects.count()

    top_projects = (
        Visitor.objects.filter(page__startswith="project:").values("page").annotate(count=Count("id")).order_by("-count")[:5]
    )
    
    total_stars = Project.objects.aggregate(Sum("github_stars"))["github_stars__sum"] or 0

    return render(request, "portfolio/analytics.html", {
        "total_visitors": total_visitors,
        "total_projects": total_projects,
        "total_messages": total_messages,
        "top_projects": top_projects,
        "total_stars": total_stars,
    })


@csrf_exempt
def github_webhook(request):
    if request.method != "POST":
        return JsonResponse({"status": "invalid request"}, status=400)
    
    try:
        sync_github()
        return JsonResponse({"status": "sync completed"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    