from django.db import models
from django.utils.text import slugify



# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    
    description = models.TextField()
    
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    
    image = models.ImageField(upload_to='project_images/', blank=True)
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    technologies = models.ManyToManyField(
        "Technology",
        blank=True
    )
    
    tags = models.JSONField(blank=True, null=True)
    is_github_project = models.BooleanField(default=False)
    
    github_stars = models.IntegerField(default=0)
    github_forks = models.IntegerField(default=0)
    github_watchers = models.IntegerField(default=0)
    github_issues = models.IntegerField(default=0)
    github_size = models.IntegerField(default=0)
    github_last_updated = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "project"
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title or "Untitled Project"
    
    def get_badges(self):
        badges = []
        
        if self.github_stars >= 10:
            badges.append("⭐ Popular")
        if self.github_last_updated:
            from django.utils import timezone
            if timezone.is_naive(self.github_last_updated):
                last_updated = timezone.make_aware(self.github_last_updated)
            else:
                last_updated = self.github_last_updated
                
            delta = timezone.now() - last_updated
            
            if delta.days <= 30:
                badges.append("🚀 Recently Updated")
        
        if self.github_forks >= 5:
            badges.append("🔥 Trending")

        if self.is_github_project:
            badges.append("🟢 Active")
            
        return badges
    
    class Meta:
        ordering = ["-id"]
    
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.email}"
 
class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField(db_index=True)
    page = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.page}"
    
class BlogPost(models.Model):
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            slug = base_slug
            counter = 1
            
            while BlogPost.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title