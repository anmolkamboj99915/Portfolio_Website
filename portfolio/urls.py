from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="home"),
    path(
        "project/<slug:slug>/", 
        views.project_detail, 
        name="project_detail"
    ),
]