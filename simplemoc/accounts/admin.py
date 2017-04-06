from django.contrib import admin

# Register your models here.
from .models import MyUser

class AccountsAdmin(admin.ModelAdmin):

	list_display = ['name', 'username', 'email','is_active', 'is_staff', 'date_joined']
	


admin.site.register(MyUser, AccountsAdmin)