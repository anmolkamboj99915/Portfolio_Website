from django.contrib import admin
from .models import Project, Skill, Category


class ProjectAdmin(admin.ModelAdmin):
    
    list_display = ("title", "category", "github_link", "live_link")
    search_fields = ("title", "description")
    list_filter = ("category",)
    
    prepopulated_fields = {"slug": ("title",)}

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill)
admin.site.register(Category)