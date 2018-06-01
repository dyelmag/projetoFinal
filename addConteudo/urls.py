from django.urls import include, path
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from . import views


app_name = 'add'
urlpatterns = [
    #path('',  views.Inicio.as_view(), name='usuario'),
    path('listar/',  views.postList.as_view(), name='listar'),
    path('listar/api/',   views.listarAPI.as_view(), name='listar-api'),
    path('manga/',  views.postManga.as_view(), name='manga'),
    path('manga/delete/<int:pk>/', views.mangaDelete.as_view(), name='mangaDelete'),
    path('manga/delete/<int:pk>/<int:cp>/',
         views.capDelete.as_view(), name='capDelete'),
    path('manga/<int:pk>/', views.mangaInfo.as_view(), name='mangaInfo'),
    path('manga/<int:pk>/api/', views.mangaInfoAPI.as_view(), name='mangaInfo-api'),
    path('manga/<int:pk>/addCap/', views.addCap.as_view(), name='addCap'),
    path('manga/<int:pk>/<int:cp>/', views.verCap.as_view(), name='capituloInfo'),
    path('manga/<int:pk>/<int:cp>/api/', views.CapituloInfoAPI.as_view(), name='capituloInfo-API'),
    path('manga/<int:pk>/<int:cp>/edt/', views.edtCap.as_view(), name='capitulo-edt'),
    path('manga/<int:pk>/<int:cp>/<int:pg>/', views.verPg.as_view(), name='pgManga'),
    path('manga/<int:pk>/<int:cp>/<int:pg>/api/', views.pgAPI.as_view(), name='pgManga-API'),
    #     name='editar-veiculo'),
    #path('novo/',   views.UsuarioNew.as_view(), name='cadastro'),
    #path('entrar/',   views.LoginView.as_view(), name='entrar'),
    #path('sair/',   views.sair, name='sair'),
    #path('editar/<int:pk>/', views.VeiculosEdit.as_view(),
    #     name='editar-veiculo'),
    #path('excluir/<int:pk>/',  views.VeiculosDelete.as_view(),
    #     name='deletar-veiculo'),
]
