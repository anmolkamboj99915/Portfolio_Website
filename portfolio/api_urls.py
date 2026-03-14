from django.urls import path
from .api_views import (
    ProjectListAPI, 
    ProjectDetailAPI, 
    SkillListAPI, 
    CategoryListAPI,
)

urlpatterns = [
    path("projects/", ProjectListAPI.as_view(), name="api_projects"),
    path("projects/<slug:slug>/", ProjectDetailAPI.as_view(), name="api_project_detail"),
    
    path("skills/", SkillListAPI.as_view(), name="api_skills"),
    path("categories/", CategoryListAPI.as_view(), name="api_categories"),
]
