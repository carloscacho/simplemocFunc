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
    url(r'^recuperar/$', 
        accounts_view.password_reset,
         name='reset' ),
    url(r'^comfirmar-recuperar/(?P<key>\w+)/$', 
        accounts_view.password_reset_confirm,
         name='password_reset_confirm' ),
    url(r'^sair/$', 
    	accounts_views_django.logout,
    	{'next_page': 'home'},name='logout' ),
    url(r'^editar/$', 
        accounts_view.edit,
         name='edit' ),
    url(r'^editar-senha/$', 
        accounts_view.edit_password,
         name='edit_password' ),
   ]