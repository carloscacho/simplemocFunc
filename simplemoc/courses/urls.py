from django.conf.urls import url, include
from simplemoc.courses import views as courses_views

urlpatterns =[

    url(r'^$', courses_views.courses, name='courses' ),
    # url(r'^(?P<pk>\d+)/$', courses_views.details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/$', courses_views.details, name='details'),
]