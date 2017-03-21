from django.conf.urls import url, include
from django.contrib.auth import views as accounts_views_django
from simplemoc.accounts import views as accounts_view
urlpatterns =[
	 url(r'^$', 
    	accounts_view.dashboard,
    	 name='dashboard'),
    url(r'^login/$', 
    	accounts_views_django.login,
    	{'template_name': 'accounts/login.html'},
    	 name='login' ),
    url(r'^cadastro/$', 
    	accounts_view.register,
    	 name='register' ),
    url(r'^sair/$', 
    	accounts_views_django.logout,
    	{'next_page': 'home'},name='logout' ),
   ]