from rest_framework import serializers
from .models import Conteudo, Manga, Capitulos, Arquivos
from django.contrib.auth.models import User 

class mangaSerializer(serializers.ModelSerializer):
    autor1 = serializers.ReadOnlyField(source='autor.first_name')

    class Meta:
        model = Manga
        fields = ('id', 'autor', 'capa', 'titulo', 'tags', 'descricao', 'status', 'dtp', 'autor1')

class capituloSerializer(serializers.ModelSerializer):

    class Meta:
        model = Capitulos      
        fields = ('id', 'manga', 'titulo', 'cpN', 'capa', 'resumo')

class arquivosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Arquivos      
        fields = ('id', 'capitulo', 'ordem', 'aquivos')


class mangaDetalhes(serializers.Serializer):
    manga = mangaSerializer(many=False)
    cap = capituloSerializer(many=True)

    class Meta:
        fields = ('manga', 'cap')

class capituloDetalhes(serializers.Serializer):
    cap = capituloSerializer(many=False)
    arq = arquivosSerializer(many=True)

    class Meta:
        fields = ('cap', 'arq')

class totalSere(serializers.Serializer):
    total = serializers.IntegerField()

class pgDetalhes(serializers.Serializer):
    cap = capituloSerializer(many=False)
    arq = arquivosSerializer(many=False)

    class Meta:
        fields = ('cap', 'arq')