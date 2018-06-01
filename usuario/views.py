#-*- coding: utf-8 -*-
#https://krzysztofzuraw.com/blog/2016/two-forms-one-view-django.html
from .models import Perfil
from addConteudo.models import Manga
from usuario.forms import FormularioUsuario, LoginUsuario, perfilM

from django.http import HttpResponseRedirect
from django.views.generic import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from .serialize import SnippetSerializer, CadastroSerializer, PerfilSerializer
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class perfilAPI(APIView):
   
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

class teste(APIView):
    serializer_class = PerfilSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Perfil.objects.get(user=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PerfilSerializer(snippet)
        return Response(serializer.data)

class entrarAPI(ObtainAuthToken):
    serializer_class = SnippetSerializer

    def post(self, request, *args, **kwargs): 
        username = self.request.POST.get('username', '')
        password = self.request.POST.get('password', '')            
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)      
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'nome': user.username
                })
            else:
                return Response({
                    'erro': 1
                })
        else:
            return Response({
                    'erro': 2
                })



class UsuarioNew(CreateView):

    model = User
    form_class = FormularioUsuario
    template_name = 'usuario/novo.html'
    success_url = reverse_lazy('inicio')

class UsuarioNewAPI(APIView):
    serializer_class = CadastroSerializer

    def post(self, validated_data):
        user = User.objects.create(
            username=self.request.POST.get('username', ''),
            email=self.request.POST.get('email', ''),
            first_name=self.request.POST.get('first_name', ''),
            last_name=self.request.POST.get('last_name', '')
        )

        user.set_password(self.request.POST.get('password', ''))
        user.save()
        
        return user




class LoginView(FormView):
    
    success_url = reverse_lazy('inicio')
    template_name = 'usuario/entrar.html'
    form_class = LoginUsuario        
    def post(self, request):
        username = self.request.POST.get('username', '')
        password = self.request.POST.get('password', '')            
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return(redirect('inicio'))
            else:
                print ("Sua conta foi desabilitada!")
        else:
            print ("Seu username e senha estavam incorretos.21111")

class infoPerfil(DetailView):
    queryset = User.objects.all()
    template_name = 'usuario/perfilInfo.html'
    def get_context_data(self, **kwargs):
        context = kwargs
        context['mangas'] = Manga.objects.filter(autor=context['object'].id)
        return context

class editarPerfil(UpdateView, LoginRequiredMixin):
    model = User
    form_class = perfilM
    template_name = 'usuario/perfilEdt.html'

    def get_success_url(self, **kwargs):
        print(self.request.user.id)
        if kwargs != None:
            return reverse_lazy('usuario:perfil', kwargs={'pk': self.request.user.id})
        else:
            return reverse_lazy('usuario:perfil', args=(self.request.user.id,))

    def get_form_kwargs(self):
        kwargs = super(editarPerfil, self).get_form_kwargs()
        if self.request.user == kwargs['instance']:
            kwargs.update(instance={
                'user': self.object,
                'perfil': self.object.perfil,
            })
            return kwargs
        else:
            raise PermissionDenied()


def sair(request):
    logout(request)
    return (redirect('/'))
