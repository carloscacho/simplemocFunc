from django.test import TestCase
from django.test.client import Client
from django.core import mail
from django.urls import reverse
from django.conf import settings

from simplemoc.courses.models import Course

# Create your tests here.

class ContactCourseTestCase(TestCase):

    def setUp(self):
        self.course = Course.objects.create(name='Django', slug='dj')
    
    def tearDown(self):
        self.course.delete()
    
    def test_contact_form_erros(self):
        data = {'name': 'fulano', 'email': '', 'message': '' }
        client = Client()
        path = reverse('details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_contact_form_success(self):
        data = {'name': 'fulano', 'email': 'admin@admin.com', 'message': 'Oi' }
        client = Client()
        path = reverse('details', args=[self.course.slug])
        response = client.post(path, data)
        # verifica se um email foi enviado
        self.assertEqual(len(mail.outbox),1)
        #verifica se o email enviado é para o contato do settinsgs
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])