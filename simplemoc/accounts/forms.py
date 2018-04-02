from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from simplemoc.core.mail import send_mail_template
from simplemoc.core.utils import generate_hash_key

from .models import PasswordReset

User = get_user_model()


class PasswordResetForm(forms.Form):

    email = forms.EmailField(label='E-mail')

    email.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            'Nenhum usuário encontrado com este e-mail'
        )

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        subject = 'Criar nova senha no Simple MOOC'
        context = {
            'reset': reset,
        }
        send_mail_template(subject, template_name, context, [user.email])

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

'''
formulario de registro do usuário
Esse form trabalha com valição da senha
'''
class RegisterForm(forms.ModelForm):

    # campos de senha e confirma senha
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput
    )

    password1.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
    
    #metodo que verifica se senha e confimação de senha, estão iguais 
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2

    # metodo que salva o registro do usuário caso está tudo ok
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    #meta que define qual o model e qual são os outros campos que serão requisitados no registro
    class Meta:
        model = User
        fields = ['username', 'email']


'''

form para editar informação do usuário

'''
class EditAccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['username', 'email', 'name']