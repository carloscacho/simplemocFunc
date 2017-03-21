from django.conf.urls import url
from simplemoc.core import views as main_views

urlpatterns = [
    url(r'^$', main_views.home, name="home"),
    url(r'^contato/$', main_views.contact, name='contact'),
]