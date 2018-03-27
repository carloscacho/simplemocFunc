from django import forms 
from django.core.mail import send_mail
from django.conf import settings

from .models import Comment

class ContactCourse(forms.Form):
	name = forms.CharField(label='Nome',
		max_length=100
		)
	
	email = forms.EmailField(label='E-mail', 
		required=True)

	message = forms.CharField(
		label='Messagens/Dúvidas',
		widget=forms.Textarea)
		
	name.widget.attrs.update({'class': 'form-control'})
	email.widget.attrs.update({'class': 'form-control'})
	message.widget.attrs.update({'class': 'form-control'})

	def send_mail(self, course):
		subject = '[%s] contato' % course
		message = 'Nome: %(name)s; Email: %(email)s; %(message)s'

		context = {
			'name': self.cleaned_data['name'],
			'email': self.cleaned_data['email'],
			'message': self.cleaned_data['message']
		}

		message = message % context 

		send_mail(
			subject, message, 
			settings.DEFAULT_FROM_EMAIL, 
			[settings.CONTACT_EMAIL]
		)

class commentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['comment']
