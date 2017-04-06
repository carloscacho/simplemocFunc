from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import extras
from django.contrib.auth import get_user_model 

MyUser = get_user_model()

class PasswordResetForm(forms.Form):
	email = forms.EmailField(label='E-mail')

	def clean_email(self):
		email = self.cleaned_data['email']
		if MyUser.object.filter(email=email).exists():
			return email
		raise forms.ValidationError('Nenhum usuário encontrado com este e-mail')


class RegisterForm(forms.ModelForm):

	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirmação de Senha', 
		widget=forms.PasswordInput)

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('A confirmação de senha não está correta')

		return password2

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

	class Meta:
		model = MyUser
		fields = ['username', 'email']

class EditAccountForm(forms.ModelForm):

	class Meta:
		model = MyUser
		fields = ['username', 'email', 'name']
		