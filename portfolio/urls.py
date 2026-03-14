from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProjectSitemap

sitemaps = {
    "projects": ProjectSitemap,
}

urlpatterns = [
    path("", views.index, name="home"),
    path(
        "project/<slug:slug>/", 
        views.project_detail, 
        name="project_detail"
    ),
    path("analytics/", views.analytics, name="analytics"),
    path(
        "sitemap.xml",
        sitemap,
        kwargs={"sitemaps": sitemaps},
        name="sitemap"
    ),
    path("github-webhook/", views.github_webhook, name="github_webhook"),
]