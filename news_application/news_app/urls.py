from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_article, name='create_article'),
    path('my_articles/', views.my_articles, name='my_articles'),
    path('approve/', views.approve_articles, name='approve_articles'),
    path('update/<int:article_id>/', views.update_article, name='update_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
]
