from django.contrib import admin
from .models import Project, Skill, Category, Contact, Technology, Visitor, BlogPost


class ProjectAdmin(admin.ModelAdmin):
    
    list_display = ("title", "slug", "category", "github_link", "live_link")
    search_fields = ("title", "description")
    list_filter = ("category",)
    list_select_related = ("category",)

    ordering = ("-id",)
    
    prepopulated_fields = {"slug": ("title",)}

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Technology)
admin.site.register(Visitor)
admin.site.register(BlogPost)