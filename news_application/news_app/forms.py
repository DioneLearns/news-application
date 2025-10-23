"""
Form definitions for news application.

Model forms for Article and Newsletter with Bootstrap styling
and validation rules for content creation.
"""

from django import forms
from .models import Article, Newsletter

class ArticleForm(forms.ModelForm):
    """
    Form for creating and editing news articles.
    
    Handles article data validation and provides form interface
    for journalists to submit and manage their content.
    
    Meta:
        model: Article model for form binding
        fields: Specified article attributes for form inclusion
    """
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }

class NewsletterForm(forms.ModelForm):
    """
    Form for creating and editing email newsletters.
    
    Manages newsletter content and metadata with validation
    for journalist submissions and editorial review.
    
    Meta:
        model: Newsletter model for form binding  
        fields: Specified newsletter attributes for form inclusion
    """
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }
