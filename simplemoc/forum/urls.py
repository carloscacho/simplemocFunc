from django.conf.urls import url, include
from simplemoc.forum.views import indexForum

urlpatterns = [
    url(r'^$', indexForum, name="forum"),
    url(r'^tag/(?P<tag>[\w_-]+)$', indexForum, name="forum_tagged"),

]
