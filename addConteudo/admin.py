from django.contrib import admin
from .models import Conteudo, Manga, Arquivos, Capitulos, Comentario, Avaliacao
# Register your models here.
admin.site.register(Conteudo)
admin.site.register(Manga)
admin.site.register(Arquivos)
admin.site.register(Capitulos)
admin.site.register(Comentario)
admin.site.register(Avaliacao)