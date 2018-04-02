"""simplemoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from simplemoc.core import urls as core_urls
from simplemoc.courses import urls as courses_urls
from simplemoc.accounts import urls as accounts_urls

from django.conf import settings 
from django.conf.urls.static import static 

admin.autodiscover()

urlpatterns = [
    url(r'^', include('simplemoc.core.urls'), name='home'),
    url(r'^cursos/', include('simplemoc.courses.urls')),
    url(r'^contas/', include('simplemoc.accounts.urls')),
    url(r'^forum/', include('simplemoc.forum.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT)
