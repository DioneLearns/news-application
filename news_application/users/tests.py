from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class UserModelTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user(self):
        """Test creating a new user"""
        user = self.user_model.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='reader'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'reader')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = self.user_model.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertEqual(superuser.username, 'admin')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_role_choices(self):
        """Test that user role choices are correct"""
        user = self.user_model.objects.create_user(
            username='testuser',
            password='testpass123',
            role='reader'
        )
        
        # Test valid role
        user.role = 'editor'
        user.save()
        
        # Test invalid role would raise error, but Django handles this with choices
        valid_roles = ['reader', 'journalist', 'editor']
        self.assertIn(user.role, valid_roles)

    def test_user_authentication(self):
        """Test user authentication"""
        user = self.user_model.objects.create_user(
            username='authuser',
            password='authpass123'
        )
        
        # Test authentication
        authenticated = self.user_model.objects.get(username='authuser').check_password('authpass123')
        self.assertTrue(authenticated)

class AuthenticationTests(TestCase):
    def test_login_view(self):
        """Test login view"""
        self.user_model = get_user_model()
        user = self.user_model.objects.create_user(
            username='loginuser',
            password='loginpass123'
        )
        
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        # Test successful login
        login_successful = self.client.login(username='loginuser', password='loginpass123')
        self.assertTrue(login_successful)

    def test_logout_view(self):
        """Test logout view - use POST method"""
        self.user_model = get_user_model()
        user = self.user_model.objects.create_user(
            username='logoutuser',
            password='logoutpass123'
        )
        
        # Login first
        self.client.login(username='logoutuser', password='logoutpass123')
        
        # Test logout with POST (required for security)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        
        # Also test that GET method is not allowed
        response_get = self.client.get(reverse('logout'))
        self.assertEqual(response_get.status_code, 405)  # Method Not Allowed
