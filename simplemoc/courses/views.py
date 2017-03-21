from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Course
from .forms import ContactCourse

def courses(request):
	courses = Course.objects.all()

	template_name = 'courses/index.html'

	context  = {
		'courses' : courses
	}

	return render(request, template_name, context)

def details(request, slug):
	course = get_object_or_404(Course, slug=slug)

	context = {}
	if request.method == 'POST':
		formCouse = ContactCourse(request.POST)
		if formCouse.is_valid():
			context['isValid'] = True
			formCouse.send_mail(course)
			formCouse = ContactCourse()

	else:
		formCouse = ContactCourse()




	context['course'] = course
	context['form'] = formCouse
	

	template_name = 'courses/details.html'
	return render(request, template_name, context)
