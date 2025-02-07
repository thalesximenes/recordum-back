from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

class Informacoe(models.Model):
    usuario = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
    escolaridade = models.CharField(max_length=100)
    vestibulares = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    universidade = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.vestibulares

class InformacoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informacoe
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        
class CadastroSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)
    escolaridade = serializers.CharField()
    vestibulares = serializers.CharField()
    curso = serializers.CharField()
    universidade = serializers.CharField()
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email já cadastrado.")
        return value

class LoginSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField(max_length=60)
    
class InformacaoSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    escolaridade = serializers.CharField()
    vestibulares = serializers.CharField()
    curso = serializers.CharField()
    universidade = serializers.CharField()