from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from wagtail.models import Site, Page
from home.models import HomePage, BlogIndexPage, BlogPage

User = get_user_model()


class SmokeTestCase(TestCase):
    """Basic smoke tests to ensure the application is working"""

    def setUp(self):
        self.client = Client()

    def test_homepage_returns_200(self):
        """Test that the homepage loads successfully"""
        response = self.client.get('/')
        # May redirect to Wagtail's default page initially
        self.assertIn(response.status_code, [200, 302])

    def test_admin_page_accessible(self):
        """Test that the admin login page is accessible"""
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)

    def test_admin_login(self):
        """Test admin user can log in"""
        # Create admin user
        admin = User.objects.create_superuser(
            username='testadmin',
            email='test@example.com',
            password='testpass123'
        )

        # Attempt login
        login_successful = self.client.login(
            username='testadmin',
            password='testpass123'
        )
        self.assertTrue(login_successful)

        # Access admin dashboard
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)


class PageModelTestCase(TestCase):
    """Test Wagtail page models"""

    def setUp(self):
        # Get root page
        self.root_page = Page.objects.get(id=1)

    def test_can_create_homepage(self):
        """Test HomePage model creation"""
        home_page = HomePage(
            title='Test Home',
            slug='test-home',
            hero_title='Test Hero',
            hero_subtitle='Test Subtitle',
        )
        self.root_page.add_child(instance=home_page)
        home_page.save_revision().publish()

        # Verify page was created
        self.assertTrue(HomePage.objects.filter(title='Test Home').exists())
        self.assertEqual(home_page.hero_title, 'Test Hero')

    def test_can_create_blog_structure(self):
        """Test blog page structure creation"""
        # Create home page
        home_page = HomePage(
            title='Home',
            slug='home',
        )
        self.root_page.add_child(instance=home_page)

        # Create blog index
        blog_index = BlogIndexPage(
            title='Blog',
            slug='blog',
        )
        home_page.add_child(instance=blog_index)

        # Create blog post
        from datetime import date
        blog_post = BlogPage(
            title='Test Post',
            slug='test-post',
            date=date.today(),
            author='Test Author',
            intro='Test intro text',
        )
        blog_index.add_child(instance=blog_post)

        # Verify structure
        self.assertEqual(blog_post.get_parent(), blog_index)
        self.assertEqual(blog_index.get_parent(), home_page)
        self.assertTrue(blog_post.author, 'Test Author')


class CourseModelTestCase(TestCase):
    """Test Course snippet model"""

    def test_can_create_course(self):
        """Test Course model creation"""
        from home.models import Course

        course = Course.objects.create(
            title='Test Course',
            subtitle='Test Subtitle',
            description='Test description',
            price=99.99,
            gumroad_link='https://gumroad.com/test',
            featured=True
        )

        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.price, 99.99)
        self.assertTrue(course.featured)
        self.assertEqual(str(course), 'Test Course')


class SettingsTestCase(TestCase):
    """Test Django settings configuration"""

    def test_settings_configured(self):
        """Test that essential settings are configured"""
        from django.conf import settings

        # Check essential settings exist
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertTrue(hasattr(settings, 'DATABASES'))
        self.assertTrue(hasattr(settings, 'STATIC_URL'))
        self.assertTrue(hasattr(settings, 'MEDIA_URL'))

        # Check Wagtail settings
        self.assertTrue(hasattr(settings, 'WAGTAIL_SITE_NAME'))

        # Check middleware
        self.assertIn('whitenoise.middleware.WhiteNoiseMiddleware', settings.MIDDLEWARE)