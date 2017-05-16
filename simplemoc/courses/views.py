from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Create your views here.
from .models import Course, Enrollment, Lesson, Material
from .forms import ContactCourse, commentForm

from django.contrib.auth.decorators import login_required

from .decorators import enrollment_required

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

@login_required
def enrollment(request, slug):
	course = get_object_or_404(Course, slug=slug)
	enrollment, created = Enrollment.objects.get_or_create(
		user=request.user, course=course)

	if created:
		enrollment.active()
		messages.success(request, 'Você foi inscrito no curso com sucesso')
	else:
		messages.info(request, 'Você Já está inscrito no Curso')
	return redirect('dashboard')

@login_required
def undo_enrollment(request, slug):
	course = get_object_or_404(Course, slug=slug)
	enrollment = get_object_or_404( Enrollment,
			user=request.user, course=course
			)
	if request.method == 'POST':
		enrollment.delete()
		messages.success(request,"Sua inscrição foi cancelada com sucesso")
		return redirect('dashboard')

	template_name = 'courses/undo_enrollment.html'
	context = {
		'enrollment': enrollment,
		'course': course,
	}

	return render(request, template_name, context)

@login_required
@enrollment_required
def course_page(request, slug):
	course = request.course
	template_name = 'courses/course_page.html'
	context = {
		'course': course,
		'announcements': course.announcements.all(),
	}
	return render(request, template_name, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
	course = request.course
	form = commentForm(request.POST or None)
	announcement = get_object_or_404(course.announcements.all(), pk=pk)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.user = request.user
		comment.announcement = announcement
		comment.save()
		form = commentForm()
		messages.success(request, 'Seu commentário foi enviado com sucesso')
	template_name = 'courses/show_announcement.html'
	
	context = {
		'course': course,
		'announcement': announcement,
		'form': form,
	}
	return render(request,template_name, context)


@login_required
@enrollment_required
def lessons(request, slug):
	course = request.course
	template_name = 'courses/lessons.html'
	lessons = course.release_lessons()
	if request.user.is_staff:
		lesson = course.lessons.all()
	context = {
		'course': course
	}
	return render(request, template_name, context)

@login_required
@enrollment_required
def informations(request, slug):
	course = request.course
	template_name = 'courses/informations.html'
	lessons = course.lessons.all()
	context = {
		'course': course,
		'lessons' : lessons
	}
	return render(request, template_name, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
	course = request.course
	lesson = get_object_or_404(Lesson, pk=pk, course=course)
	if not request.user.is_staff and not lesson.is_available():
		messages.error(request, 'Está aula não está disponivel')
		return redirect('lessons', slug=course.slug)
	template_name = 'courses/lesson.html'
	context = {
		'course': course,
		'lesson': lesson,
	}

	return render(request, template_name, context)

@login_required
@enrollment_required
def material(request, slug, pk):
	course = request.course
	material = get_object_or_404(Material, pk=pk, lesson__course=course)
	lesson = material.lesson
	if not request.user.is_staff and not lesson.is_available():
		messages.error(request, 'Este material não está disponivel')
		return redirect('lesson', slug=course.slug, pk=lesson.pk)
	template_name = 'courses/material.html'
	context = {
		'course': course,
		'lesson': lesson,
		'material': material,
	}

	return render(request, template_name, context)