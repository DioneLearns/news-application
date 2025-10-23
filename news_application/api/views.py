from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from news_app.models import Article, Publisher
from news_app.models import CustomUser
from .serializers import ArticleSerializer, PublisherSerializer, UserSerializer

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows articles to be viewed.
    Articles are filtered based on user subscriptions.
    """
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Article.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        queryset = Article.objects.filter(is_approved=True)
        
        # If user is a reader, show only articles from their subscriptions
        if user.role == 'reader':
            # Get user's subscriptions
            subscribed_publishers = user.subscribed_publishers.all()
            subscribed_journalists = user.subscribed_journalists.all()
            
            # Filter articles by subscriptions
            queryset = queryset.filter(
                Q(publisher__in=subscribed_publishers) |
                Q(author__in=subscribed_journalists)
            ).distinct()
        
        # If user is journalist, show their own articles
        elif user.role == 'journalist':
            queryset = queryset.filter(author=user)
        
        # Editors can see all articles
        elif user.role == 'editor':
            queryset = Article.objects.all()
        
        return queryset.order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def my_subscriptions(self, request):
        """Get articles from current user's subscriptions"""
        if request.user.role != 'reader':
            return Response({"error": "This endpoint is for readers only"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        subscribed_publishers = request.user.subscribed_publishers.all()
        subscribed_journalists = request.user.subscribed_journalists.all()
        
        articles = Article.objects.filter(
            Q(publisher__in=subscribed_publishers) |
            Q(author__in=subscribed_journalists),
            is_approved=True
        ).distinct().order_by('-created_at')
        
        # Use pagination
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows publishers to be viewed.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        """Subscribe to a publisher"""
        if request.user.role != 'reader':
            return Response({"error": "Only readers can subscribe to publishers"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        publisher = self.get_object()
        request.user.subscribed_publishers.add(publisher)
        return Response({"status": f"Subscribed to {publisher.name}"})
    
    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        """Unsubscribe from a publisher"""
        publisher = self.get_object()
        request.user.subscribed_publishers.remove(publisher)
        return Response({"status": f"Unsubscribed from {publisher.name}"})

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see journalists (for subscription purposes)
        return CustomUser.objects.filter(role='journalist')
    
    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        """Subscribe to a journalist"""
        if request.user.role != 'reader':
            return Response({"error": "Only readers can subscribe to journalists"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        journalist = self.get_object()
        if journalist.role != 'journalist':
            return Response({"error": "Can only subscribe to journalists"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        request.user.subscribed_journalists.add(journalist)
        return Response({"status": f"Subscribed to {journalist.username}"})
    
    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        """Unsubscribe from a journalist"""
        journalist = self.get_object()
        request.user.subscribed_journalists.remove(journalist)
        return Response({"status": f"Unsubscribed from {journalist.username}"})
