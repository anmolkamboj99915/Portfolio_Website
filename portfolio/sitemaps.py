from django.contrib.sitemaps import Sitemap
from .models import Project
from django.urls import reverse

class ProjectSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.exclude(slug__isnull=True)
    
    def lastmod(self, obj):
        return obj.github_last_updated if obj.github_last_updated else None
        
    def location(self, obj):
        return reverse("project_detail", args=[obj.slug])
    
    