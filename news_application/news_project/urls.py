"""
URL configuration for news_project.

Defines all application routes including authentication, articles,
newsletters, and API endpoints with proper naming and structure.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from news_app.views import home, create_article, approve_articles, approve_article, my_articles, subscribe_journalist, subscribe_publisher
from news_app.views import create_newsletter, my_newsletters, approve_newsletters, approve_newsletter, all_newsletters, edit_newsletter, delete_newsletter
from users.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('news/', include('news_app.urls')),  
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('articles/create/', create_article, name='create_article'),
    path('articles/approve/', approve_articles, name='approve_articles'),
    path('articles/approve/<int:article_id>/', approve_article, name='approve_article'),
    path('my-articles/', my_articles, name='my_articles'),
    path('subscribe/journalist/<int:journalist_id>/', subscribe_journalist, name='subscribe_journalist'),
    path('subscribe/publisher/<int:publisher_id>/', subscribe_publisher, name='subscribe_publisher'),
    path('api/', include('api.urls')),
    path('newsletters/create/', create_newsletter, name='create_newsletter'),
    path('my-newsletters/', my_newsletters, name='my_newsletters'),
    path('newsletters/approve/', approve_newsletters, name='approve_newsletters'),
    path('newsletters/approve/<int:newsletter_id>/', approve_newsletter, name='approve_newsletter'),
    path('newsletters/', all_newsletters, name='all_newsletters'),
    path('newsletters/edit/<int:newsletter_id>/', edit_newsletter, name='edit_newsletter'),
    path('newsletters/delete/<int:newsletter_id>/', delete_newsletter, name='delete_newsletter'),
]
