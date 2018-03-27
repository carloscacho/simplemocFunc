from django.test import TestCase
from django.test.client import Client
from django.core import mail
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

from simplemoc.courses.models import Course

# Create your tests here.

class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.courses_dj = mommy.make('courses.Course', name='Text alet com Django', _quantity=10)
        self.courses_dv = mommy.make('courses.Course', name='Dev e top', _quantity=10)
        # self.course2 = mommy.make('courses.Course', _)
        self.cliet = Client()

    
    def tearDown(self):
        for course in self.courses_dj:
            course.delete()
        for course in self.courses_dv:
            course.delete()

    def test_course_search(self):
        search = Course.objects.search('Django')
        self.assertEqual(len(search), 10)

        search = Course.objects.search('Dev')
        self.assertEqual(len(search), 10)