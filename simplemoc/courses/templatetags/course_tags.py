from django.template import Library

register = Library()

from simplemoc.courses.models import Enrollment

@register.inclusion_tag('courses/tags/my_courses.html')
def my_courses(user):
	enrollment = Enrollment.objects.filter(user=user)
	context = {
		'enrollments': enrollment
	}

	return context