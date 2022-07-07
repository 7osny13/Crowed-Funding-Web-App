from unicodedata import category
from django.db import models
from django.contrib.auth.models import User


class CategoryMain(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
  
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    goal = models.IntegerField()
    image_thumb = models.ImageField(upload_to='projects/thumb', blank=True , null=True)
    created_at = models.DateTimeField()
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    rating=models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cat_related=models.ForeignKey(CategoryMain, on_delete=models.CASCADE)
    actual_goal=models.IntegerField(default=0)
    def __str__(self):
        return self.name

    def __str__(self):
        return self.name
class Comments(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment
class MultiImages(models.Model):
    image = models.ImageField(upload_to='projects/multi', blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.image.url

    
class Tago(models.Model):
    tagg=models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectReport(models.Model):
    project = models.IntegerField()
    user = models.IntegerField()
    report = models.TextField()
    created_at = models.DateTimeField()
    def __str__(self):
        return self.report
class CommentsReport(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField()
    project = models.IntegerField()
    user = models.IntegerField()
    def __str__(self):
        return self.comment
class ProjectRating(models.Model):
    project = models.IntegerField()
    user = models.IntegerField()
    rating = models.IntegerField()
    created_at = models.DateTimeField()
 
class ProjectDonation(models.Model):
    project = models.IntegerField()
    user = models.IntegerField()
    donation = models.IntegerField()
    created_at = models.DateTimeField()
    def __str__(self):
        return self.donation

