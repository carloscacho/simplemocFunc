from django.contrib import admin

# Register your models here.
from .models import Course, Enrollment, Comment, Announcement, Lesson, Material

class CourseAdmin(admin.ModelAdmin):

	list_display = ['name', 'slug', 'start_date', 'created_at']
	search_fields = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}


class MaterialInlineAdmin(admin.TabularInline):
	model = Material

class EnrollmentAdmin(admin.ModelAdmin):
	list_display = ['user', 'course', 'status', 'created_at']
	search_fields = ['user', 'course']
	list_filter = ['created_at']

class LessonAdmin(admin.ModelAdmin):
	list_display = ['name', 'number', 'course', 'relase_date']
	search_fields = ['name', 'description']
	list_filter = ['created_at']

	inlines= [MaterialInlineAdmin]

class CommentAdmin(admin.ModelAdmin):
	list_display = ['user', 'announcement', 'comment', 'created_at']
	search_fields = ['user', 'announcement']
	list_filter = ['created_at']

class AnnouncementAdmin(admin.ModelAdmin):
	list_display = ['course', 'title', 'created_at']
	search_fields = ['course', 'title']
	list_filter = ['created_at']

admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Lesson, LessonAdmin)