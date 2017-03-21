from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import extras
from django.contrib.auth.models import User 


class RegisterForm(UserCreationForm):

	email = forms.EmailField(label='E-mail')
	dayNasc = forms.DateField(label='Data de Nacimento', widget=extras.SelectDateWidget(years=range(1900, 2100)))

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Já existe um usuário com este E-mail')
		return email

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.dayNasc = self.cleaned_data['dayNasc']
		if commit:
			user.save()
		return user