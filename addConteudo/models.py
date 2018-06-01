from django.db import models
from django.contrib.auth.models import User

class Conteudo(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    capa = models.ImageField(upload_to='media', blank=True)
    tipo = models.IntegerField()
    titulo = models.CharField(max_length=250)
    dnp = models.DateField(null=True, blank=True)
    tags = models.CharField(max_length=250)
    descricao = models.TextField(blank=True)

def user_directory_path(instance, filename):
    return 'mangas/manga_{0}/{1}'.format(instance.id, filename)

class Manga(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    tags = models.CharField(max_length=250)
    dtp = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True)
    status = models.IntegerField()
    capa = models.FileField(upload_to=user_directory_path)

class Capitulos(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250, blank=True)
    cpN = models.IntegerField()
    capa = models.FileField()
    resumo = models.TextField(blank=True)

def user_directory_path2(instance, filename):
    return 'mangas/manga_{0}/capitulo_{1}/{2}'.format(instance.capitulo.manga.id,instance.capitulo.id, filename)
class Arquivos(models.Model):
    capitulo = models.ForeignKey(Capitulos, on_delete=models.CASCADE)
    ordem = models.IntegerField()
    aquivos = models.FileField(upload_to=user_directory_path2)

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    dtp = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=False)

class Avaliacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    dtp = models.DateTimeField(auto_now_add=True)
    nota = models.IntegerField()