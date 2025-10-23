"""
Form definitions for news application.

Model forms for Article and Newsletter with Bootstrap styling
and validation rules for content creation.
"""

from django import forms
from .models import Article, Newsletter

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }
