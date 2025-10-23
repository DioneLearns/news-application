from rest_framework import serializers
from news_app.models import Article, Publisher
from news_app.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'description',]

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'author', 'publisher',
            'created_at', 'is_approved', 'approved_by'
        ]
        read_only_fields = ['id','author',]
