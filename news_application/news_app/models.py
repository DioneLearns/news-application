"""
Database models for news application.

Defines Publisher, Article, and Newsletter models with relationships
and business logic for the news publishing system.
"""

from django.contrib.auth.models import Group
from django.db import models
from users.models import CustomUser  # Import from users app

class Publisher(models.Model):
    """
    Represents a publishing entity that produces news content.

    Publishers are organizations that manage editors and journalists
    and oversee article publication workflows.

    Attributes:
        name (CharField): The official name of the publishing company
        description (TextField): Detailed information about the publisher
        editors (ManyToManyField): Users with editor role assigned to this publisher
        journalists (ManyToManyField): Users with journalist role assigned to this publisher
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    editors = models.ManyToManyField(CustomUser, related_name='publisher_editors', limit_choices_to={'role': 'editor'})  
    journalists = models.ManyToManyField(CustomUser, related_name='publisher_journalists', limit_choices_to={'role': 'journalist'})  

    def __str__(self):
        return self.name  

class Article(models.Model):
    """
    Represents an individual news article in the publishing system.

    Stores article content, metadata, workflow status, and relationships
    to authors, publishers, and newsletters.

    Attributes:
        title (CharField): The headline or title of the article
        content (TextField): The main body text of the article  
        author (ForeignKey): The journalist user who wrote this article
        publisher (ForeignKey): The publishing organization
        is_approved (BooleanField): Whether article has editorial approval
        created_at (DateTimeField): Automatic timestamp when article was created
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'journalist'})  
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Newsletter(models.Model):
    """
    Represents an email newsletter containing curated articles.

    Newsletters are periodic email distributions that feature
    selected articles for subscriber consumption.

    Attributes:
        title (CharField): The name or subject line of the newsletter
        content (TextField): The main body content of the newsletter
        author (ForeignKey): The journalist user who created this newsletter
        publisher (ForeignKey): The associated publishing organization
        is_approved (BooleanField): Whether newsletter has editorial approval
        created_at (DateTimeField): Automatic timestamp when newsletter was created
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'journalist'})  
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title