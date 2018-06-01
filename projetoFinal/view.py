from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class Inicio(TemplateView):

    template_name = 'inicio.html'
