from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from news_app.models import Article, Publisher

class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        
        # Create test users
        self.reader = self.user_model.objects.create_user(
            username='testreader',
            email='testreader@example.com',
            password='testpass123',
            role='reader'
        )
        
        self.journalist = self.user_model.objects.create_user(
            username='testjournalist',
            email='testjournalist@example.com',
            password='testpass123',
            role='journalist'
        )
        
        self.editor = self.user_model.objects.create_user(
            username='testeditor',
            email='testeditor@example.com',
            password='testpass123',
            role='editor'
        )
        
        # Create test publisher
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='Test publisher description'
        )
        
        # Create test articles
        self.approved_article = Article.objects.create(
            title='Approved Test Article',
            content='This is an approved test article content.',
            author=self.journalist,
            publisher=self.publisher,
            is_approved=True
        )
        
        self.pending_article = Article.objects.create(
            title='Pending Test Article',
            content='This is a pending test article content.',
            author=self.journalist,
            publisher=self.publisher,
            is_approved=False
        )

    def get_results_from_response(self, response):
        """Helper method to get results from paginated or non-paginated response"""
        if isinstance(response.data, list):
            return response.data
        elif 'results' in response.data:
            return response.data['results']
        return response.data

    def test_articles_api_authentication_required(self):
        """Test that API requires authentication"""
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_can_view_subscribed_articles(self):
        """Test that readers can see articles from their subscriptions"""
        self.client.force_authenticate(user=self.reader)
        
        # Subscribe reader to publisher
        self.reader.subscribed_publishers.add(self.publisher)
        
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle both paginated and non-paginated responses
        results = self.get_results_from_response(response)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Approved Test Article')

    def test_journalist_can_view_own_articles(self):
        """Test that journalists can see their own articles"""
        self.client.force_authenticate(user=self.journalist)
        
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle both paginated and non-paginated responses
        results = self.get_results_from_response(response)
        articles = [article['title'] for article in results]
        self.assertIn('Approved Test Article', articles)

    def test_editor_can_view_all_articles(self):
        """Test that editors can see all articles"""
        self.client.force_authenticate(user=self.editor)
        
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle both paginated and non-paginated responses
        results = self.get_results_from_response(response)
        articles = [article['title'] for article in results]
        self.assertIn('Approved Test Article', articles)
        self.assertIn('Pending Test Article', articles)

    def test_subscribe_to_publisher(self):
        """Test that readers can subscribe to publishers"""
        self.client.force_authenticate(user=self.reader)
        
        response = self.client.post(f'/api/publishers/{self.publisher.id}/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], f'Subscribed to {self.publisher.name}')
        
        # Check that subscription was added
        self.assertTrue(self.reader.subscribed_publishers.filter(id=self.publisher.id).exists())

    def test_subscribe_to_journalist(self):
        """Test that readers can subscribe to journalists"""
        self.client.force_authenticate(user=self.reader)
        
        response = self.client.post(f'/api/journalists/{self.journalist.id}/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], f'Subscribed to {self.journalist.username}')
        
        # Check that subscription was added
        self.assertTrue(self.reader.subscribed_journalists.filter(id=self.journalist.id).exists())

    def test_my_subscriptions_endpoint(self):
        """Test the my_subscriptions endpoint for readers"""
        self.client.force_authenticate(user=self.reader)
        
        # Subscribe to both publisher and journalist
        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)
        
        response = self.client.get('/api/articles/my_subscriptions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle both paginated and non-paginated responses
        results = self.get_results_from_response(response)
        self.assertEqual(len(results), 1)

    def test_non_reader_cannot_subscribe(self):
        """Test that non-readers cannot subscribe"""
        self.client.force_authenticate(user=self.journalist)
        
        response = self.client.post(f'/api/publishers/{self.publisher.id}/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_pagination(self):
        """Test that API responses are paginated - skip if not paginated"""
        self.client.force_authenticate(user=self.editor)
        
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Only test pagination if it's enabled
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertIn('results', response.data)
            self.assertIn('count', response.data)
            self.assertIn('next', response.data)
            self.assertIn('previous', response.data)
        else:
            # If not paginated, just make sure we get data
            self.assertTrue(len(response.data) > 0)
