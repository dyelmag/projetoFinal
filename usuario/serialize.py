from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil

class SnippetSerializer(serializers.ModelSerializer):
    teste = 'aaaaaaaaaa'
    class Meta:
        model = User
        fields = ('id', 'first_name')

class CadastroSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password', 'username',
                 'first_name', 'last_name', 'email']
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class PerfilSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user.first_name')
    Lname = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Perfil
        fields = ('id', 'capa', 'dn', 'sobre', 'cidade',
                  'name', 'Lname', 'email')
    
