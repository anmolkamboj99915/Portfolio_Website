from django.db import models
from django.utils.text import slugify



# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    
    description = models.TextField()
    
    github_link = models.URLField()
    live_link = models.URLField()
    
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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class Skill(models.Model):
    name = models.CharField(max_length=100)
    
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
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name