from django.contrib import admin

# Register your models here.
from .models import MyUser

'''
Somente para registro de uma area para criação de usuarios pelo Admin
Devido a mudança do Registro de Usuarios Padrão do Django
é nessario cirar o propio ModelAdmin para que admin tenha acesso 
'''
class AccountsAdmin(admin.ModelAdmin):

	list_display = [ 'username', 'name', 'email','is_active', 'is_staff', 'date_joined']
	


admin.site.register(MyUser, AccountsAdmin)