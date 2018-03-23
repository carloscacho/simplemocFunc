import re

from django.db import models
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.conf import settings


'''
Modelo para criação da tabela no Banco dos Usuários
Essa é uma mudança nos User Padrão do Django.
Para que não ocorra erros alguns coisas devem ser 
similar ao User padrão do Djando

AbstractBaseUser: Usuário padrão do Django que será extendo por esse novo padrão
PermissionsMixin: classe que realiza a premisão de acesso do usuário
'''

class MyUser(AbstractBaseUser, PermissionsMixin):
	##User validators.RegexValidator()
	username = models.CharField('Nome do Usuário', max_length=30, unique=True,
		validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), 
			'Nome do Usuário só pode conter letras, digitos ou os seguintes caracteres: @/./+/-/_','invalid')])
	email = models.EmailField('E-mail', unique=True)
	name = models.CharField('Nome Completo', max_length=100, blank=True)
	is_active = models.BooleanField('Está ativo?', blank=True, default=True)
	is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
	date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)
	is_trusty = models.BooleanField(_('trusty'), default=False,
		help_text=_('Designates whether this user has confirmed his account.'))
	
	objects = UserManager()

	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']


	def __str__(self):
		return self.name or self.username

	def get_short_name(self):
		return self.username

	def get_full_name(self):
		return str(self)

	class Meta:
		verbose_name='Usuário'
		verbose_name_plural = 'Usuários'



'''
Modelo para requisição de pedidos de nova senha
Acionado caso o usuário esqueça a senha
'''
class PasswordReset(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL,
		verbose_name='Usuário', 
		related_name='resets', 
		on_delete=models.CASCADE)

	key = models.CharField('Chave reset', max_length=50, unique=True)
	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	confirmed = models.BooleanField('confirmado? ', default=False, blank=True)

	def __str__(self):
		return '{0} em {1}'.format(self.user, self.created_at)


	class Meta:
		verbose_name='Nova Senha'
		verbose_name_plural = 'Novas Senhas'
		ordering = ['-created_at']