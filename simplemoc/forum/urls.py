from django.conf.urls import url, include
from simplemoc.forum.views import (indexForum, threadForum, replayCorrect, replayIncorrect, replayUp, replayDown)

urlpatterns = [
    url(r'^$', indexForum, name="forum"),
    url(r'^tag/(?P<tag>[\w_-]+)$', indexForum, name="forum_tagged"),
    url(r'^topico/(?P<slug>[\w_-]+)$', threadForum, name="forum_thread"),
    url(r'^respostas/(?P<pk>\d+)/correct/$', replayCorrect , name="forum_replay_correct"),
    url(r'^respostas/(?P<pk>\d+)/incorrect/$', replayIncorrect , name="forum_replay_incorrect"),
    url(r'^respostas/(?P<pk>\d+)/up/$', replayUp , name="forum_replay_up"),
    url(r'^respostas/(?P<pk>\d+)/down/$', replayDown , name="forum_replay_down")
]
