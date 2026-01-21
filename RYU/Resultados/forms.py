from django import forms

from EstructuraAcademica.models import PeriodoAcademico
from .models import Prueba

class PruebaForm(forms.ModelForm):
    class Meta:

        model = Prueba
        fields = ['nombre', 'descripcion', 'fecha']

        periodoAcademico = forms.ModelChoiceField(
            queryset=PeriodoAcademico.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            required=True,
        )
