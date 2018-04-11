from django import forms

from .models import Replay

class ReplayForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['replay'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Replay
        fields = ['replay']