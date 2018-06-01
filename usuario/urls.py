from django.urls import include, path
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from . import views
from rest_framework.authtoken import views as rest_framework_views


app_name = 'usuario'
urlpatterns = [
    path('novo/',   views.UsuarioNew.as_view(), name='cadastro'),
    path('novo/api/',   views.UsuarioNewAPI.as_view(), name='cadastro-api'),
    path('entrar/',   views.LoginView.as_view(), name='entrar'),
    path('entrar/api/',   views.entrarAPI.as_view(), name='entrar-api'),
    path('<int:pk>/', views.infoPerfil.as_view(), name='perfil'),
    path('<int:pk>/api', views.infoPerfil.as_view(), name='perfil-api'),
    path('<int:pk>/editar/',   views.editarPerfil.as_view(), name='editar-perfil'),
    path('api/',   views.teste.as_view(), name='api2'),
    path('api/<int:pk>/',   views.teste.as_view(), name='api'),
    path('sair/',   views.sair, name='sair'),
    
    #path('editar/<int:pk>/', views.VeiculosEdit.as_view(),
    #     name='editar-veiculo'),
    #path('excluir/<int:pk>/',  views.VeiculosDelete.as_view(),
    #     name='deletar-veiculo'),
]
