from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Project, Skill, Category
from .serializers import ProjectSerializer, SkillSerializer, CategorySerializer

class ProjectListAPI(ListAPIView):
    queryset = Project.objects.select_related("category").prefetch_related("technologies")
    serializer_class = ProjectSerializer
    
class ProjectDetailAPI(RetrieveAPIView):
    queryset = Project.objects.select_related("category").prefetch_related("technologies")
    serializer_class = ProjectSerializer
    lookup_field = "slug"
    
class SkillListAPI(ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    
class CategoryListAPI(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer