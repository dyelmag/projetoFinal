# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, ImageField
from django import forms
from django.contrib.auth.models import User 
from django.forms.utils import ErrorList
from .models import Perfil
from io import StringIO
from PIL import Image
from betterforms.multiform import MultiModelForm

class FormularioUsuario(forms.ModelForm):
    User._meta.get_field('email').blank = False
    User._meta.get_field('first_name').blank = False
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'maxlength': 255}))
    
    class Meta:
        model = User
        fields = ['password', 'username',
                 'first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
        }

        error_messages = {
            'first_name': {
                'required': 'Campo Obrigatorio1'
            },
            'last_name': {
                'required': 'Campo Obrigatorio2'
            },
            'email': {
                'required': 'Campo Obrigatorio'
            },
            'username': {
                'required': 'Campo Obrigatorio'
            },
            'password': {
                'required': 'Campo Obrigatorio'
            },
        }

    def save(self, commit=True):
        
        user = super(FormularioUsuario, self).save(commit=False) 
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save() 
        return user



class LoginUsuario(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['password', 'username']

        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
        }
        error_messages = {
            'username': {
                'required': 'Campo Obrigatorio'
            },
            'password': {
                'required': 'Campo Obrigatorio'
            },
        }

class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
        }

class Imagem(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html =  Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))


class edtPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'dn', 'cidade', 'sobre', 'capa'
        ]

        widgets = {
            'dn': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'maxlength': 255}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'sobre': forms.Textarea(attrs={'class': 'form-control', 'rows': 3 }),
            'capa': forms.FileInput(attrs={'class': 'form-control', 'id': 'capa_id', 'onchange': 'loadFile(event)'}),
        }

class perfilM(MultiModelForm):
    form_classes = {
        'user': EditUser,
        'perfil': edtPerfil,
    }
