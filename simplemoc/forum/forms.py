from django import forms
from taggit.forms import *

from .models import Replay, Thread

class ReplayForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['replay'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Replay
        fields = ['replay']

class ThreadForm(forms.ModelForm):
    tags_de_Busca = TagField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['body'].widget.attrs.update({'class': 'form-control'})
        self.fields['tags_de_Busca'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Thread
        fields = ['title', 'body']