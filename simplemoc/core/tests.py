from django.test import TestCase
from django.core import mail
from django.test.client import Client

# Create your tests here.
class HomeViewTest(TestCase):
    
    def test_home_status_code(self):
        client = Client()
        resp = client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_home_template_used(self):
        client = Client()
        resp = client.get('/')
        self.assertTemplateUsed(resp, 'home.html')
        self.assertTemplateUsed(resp, 'base.html')