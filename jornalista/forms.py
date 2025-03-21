from django import forms
from .models import NotíciaModel


class NoticiasForm(forms.ModelForm):
    class Meta:
        model = NotíciaModel
        fields = ['tituto', 'noticia', 'autor']