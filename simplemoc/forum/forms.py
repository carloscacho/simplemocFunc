from django import forms

from .models import Replay

class ReplayForm(forms.ModelForm):


    class Meta:
        model = Replay
        fields = ['replay']