from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser with role-based permissions.
    
    Provides enhanced user management with predefined roles (reader, journalist, editor)
    and subscription tracking for personalized content delivery.
    
    Attributes:
        role (CharField): User's system role determining permissions and access
        subscribed_journalists (ManyToManyField): Journalists user follows
        subscribed_publishers (ManyToManyField): Publishers user follows
    """
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    bio = models.TextField(max_length=500, blank=True)
    
    # Subscription fields for readers
    subscribed_journalists = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        blank=True, 
        related_name='subscribers',
        limit_choices_to={'role': 'journalist'}
    )
    subscribed_publishers = models.ManyToManyField(
        'news_app.Publisher',
        blank=True,
        related_name='subscribers'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        db_table = 'auth_user'
