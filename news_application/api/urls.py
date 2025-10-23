from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, PublisherViewSet, UserViewSet

# Create a router and register our viewsets with basename
router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'publishers', PublisherViewSet, basename='publisher')
router.register(r'journalists', UserViewSet, basename='journalist')

urlpatterns = [
    path('', include(router.urls)),
]

# Add login URLs for the browsable API
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
