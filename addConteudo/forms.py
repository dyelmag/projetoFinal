# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User 
from django.forms.utils import ErrorList
from .models import Manga, Arquivos, Capitulos

class FormularioManga(forms.ModelForm):
    
    class Meta:
        model = Manga

        fields = ['autor', 'titulo',
                    'tags', 'descricao', 'status', 'capa']
        
        widgets = {

            'titulo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'cols': 80, 'rows': 5}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'capa': forms.FileInput(attrs={'class': 'form-control', 'id': 'capa_id', 'onchange': 'loadFile(event)'})
        }
