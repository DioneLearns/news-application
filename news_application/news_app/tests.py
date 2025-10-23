from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Article, Publisher

class NewsAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        
        self.journalist = self.user_model.objects.create_user(
            username='testjournalist',
            password='testpass123',
            role='journalist'
        )
        
        self.editor = self.user_model.objects.create_user(
            username='testeditor',
            password='testpass123',
            role='editor'
        )
        
        self.reader = self.user_model.objects.create_user(
            username='testreader',
            password='testpass123',
            role='reader'
        )
        
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='Test Description'
        )
        
        self.article = Article.objects.create(
            title='Test Article',
            content='Test content',
            author=self.journalist,
            publisher=self.publisher,
            is_approved=False
        )

    def test_article_creation(self):
        """Test article creation"""
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.author, self.journalist)
        self.assertFalse(self.article.is_approved)

    def test_publisher_creation(self):
        """Test publisher creation"""
        self.assertEqual(self.publisher.name, 'Test Publisher')
        self.assertEqual(str(self.publisher), 'Test Publisher')

    def test_home_page_access(self):
        """Test that home page is accessible"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to News Application')

    def test_login_required_for_article_creation(self):
        """Test that login is required to create articles"""
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_journalist_can_create_article(self):
        """Test that journalists can access article creation"""
        self.client.login(username='testjournalist', password='testpass123')
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 200)

    def test_editor_can_approve_articles(self):
        """Test that editors can access approval page"""
        self.client.login(username='testeditor', password='testpass123')
        response = self.client.get(reverse('approve_articles'))
        self.assertEqual(response.status_code, 200)

    def test_reader_cannot_approve_articles(self):
        """Test that readers cannot access approval page"""
        self.client.login(username='testreader', password='testpass123')
        response = self.client.get(reverse('approve_articles'))
        self.assertEqual(response.status_code, 302)  # Redirect or permission denied

    def test_article_approval_process(self):
        """Test the article approval process"""
        self.client.login(username='testeditor', password='testpass123')
        
        # Approve the article
        response = self.client.get(reverse('approve_article', args=[self.article.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after approval
        
        # Refresh article from database
        self.article.refresh_from_db()
        self.assertTrue(self.article.is_approved)
        #self.assertEqual(self.article.is_approved_by, self.editor)

    def test_my_articles_page(self):
        """Test that journalists can view their articles"""
        self.client.login(username='testjournalist', password='testpass123')
        response = self.client.get(reverse('my_articles'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')

class ModelTests(TestCase):
    def test_article_str_representation(self):
        """Test Article string representation"""
        user_model = get_user_model()
        journalist = user_model.objects.create_user(username='journalist', password='test', role='journalist')
        article = Article(title='Test Article', content='Content', author=journalist)
        self.assertEqual(str(article), 'Test Article')

    def test_publisher_str_representation(self):
        """Test Publisher string representation"""
        publisher = Publisher(name='Test Publisher')
        self.assertEqual(str(publisher), 'Test Publisher')
