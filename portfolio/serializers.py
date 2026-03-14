from rest_framework import serializers
from .models import Project, Skill, Category, Technology

class TechnologySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Technology
        fields = ["id", "name"]
        

class ProjectSerializer(serializers.ModelSerializer):
    
    technologies = TechnologySerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    
    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "description",
            "image",
            "github_link",
            "live_link",
            "github_stars",
            "github_forks",
            "github_watchers",
            "github_issues",
            "tags",
            "category",
            "technologies",
        ]
        
        read_only_fields = [
            "slug",
            "github_stars",
            "github_forks",
            "github_watchers",
            "github_issues",
            "tags",
        ]
        
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name"]
        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ["id", "name"]
        