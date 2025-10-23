from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Publisher, Article, Newsletter

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    filter_horizontal = ('editors', 'journalists')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'is_approved')
    list_editable = ('is_approved',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'is_approved')
    list_editable = ('is_approved',)