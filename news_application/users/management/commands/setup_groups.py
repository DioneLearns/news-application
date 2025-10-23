from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news_app.models import Article, Publisher

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'
    
    def handle(self, *args, **kwargs):
        # Create groups
        reader_group, created = Group.objects.get_or_create(name='Reader')
        editor_group, created = Group.objects.get_or_create(name='Editor')
        journalist_group, created = Group.objects.get_or_create(name='Journalist')
        
        # Get content types
        article_content_type = ContentType.objects.get_for_model(Article)
        publisher_content_type = ContentType.objects.get_for_model(Publisher)
        
        # Get permissions
        article_permissions = Permission.objects.filter(content_type=article_content_type)
        publisher_permissions = Permission.objects.filter(content_type=publisher_content_type)
        
        # Assign permissions to Editor group
        for perm in article_permissions:
            if perm.codename in ['view_article', 'change_article', 'delete_article']:
                editor_group.permissions.add(perm)
        
        # Assign permissions to Journalist group  
        for perm in article_permissions:
            if perm.codename in ['add_article', 'view_article', 'change_article', 'delete_article']:
                journalist_group.permissions.add(perm)
        
        # Reader group gets only view permissions
        view_article = Permission.objects.get(codename='view_article')
        reader_group.permissions.add(view_article)
        
        self.stdout.write(self.style.SUCCESS('Successfully created groups and permissions'))
