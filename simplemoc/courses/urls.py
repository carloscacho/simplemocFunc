from django.conf.urls import url, include
from simplemoc.courses import views as courses_views

urlpatterns =[

    url(r'^$', courses_views.courses, name='courses' ),
    # url(r'^(?P<pk>\d+)/$', courses_views.details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/$', courses_views.details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', courses_views.enrollment, name='enrollment'),
    url(r'^(?P<slug>[\w_-]+)/course_page/$', courses_views.course_page, name='coursepage'),
    url(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$', courses_views.undo_enrollment, name='undo_enrollment'),
    url(r'^(?P<slug>[\w_-]+)/show_announcement/(?P<pk>\d+)$', courses_views.show_announcement, name='show_announcement'),
    url(r'^(?P<slug>[\w_-]+)/aulas/$', courses_views.lessons, name='lessons'),
    url(r'^(?P<slug>[\w_-]+)/aula/(?P<pk>\d+)$', courses_views.lesson, name='lesson'),
    url(r'^(?P<slug>[\w_-]+)/informações/$', courses_views.informations, name='courseinfo'),
]