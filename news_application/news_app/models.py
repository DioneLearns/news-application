"""
Database models for news application.

Defines Publisher, Article, and Newsletter models with relationships
and business logic for the news publishing system.
"""

from django.contrib.auth.models import Group
from django.db import models
from users.models import CustomUser  # Import from users app

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    editors = models.ManyToManyField(CustomUser, related_name='publisher_editors', limit_choices_to={'role': 'editor'})  
    journalists = models.ManyToManyField(CustomUser, related_name='publisher_journalists', limit_choices_to={'role': 'journalist'})  

    def __str__(self):
        return self.name  

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'journalist'})  
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'journalist'})  
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title