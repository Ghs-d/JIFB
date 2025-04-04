from django.forms import ModelForm
from .models import Noticia, ArquivoNaNoticia
from django import forms



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result



class NoticiaForm(ModelForm):
    class Meta:
        model = Noticia
        fields = '__all__'
        exclude = ['autor']

class ArquivosForm(forms.Form):
    arquivos = MultipleFileField()
    class Meta:
        model = ArquivoNaNoticia
        fields = ('arquivos',)