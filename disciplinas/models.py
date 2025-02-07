from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class EixosTematico(models.Model):
    nome = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.nome

class EixosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EixosTematico
        fields="__all__"

class Disciplinas(models.Model):
    nome = models.CharField(max_length = 100)
    thumb = models.CharField(max_length= 500)
    eixo = models.ForeignKey(EixosTematico, on_delete = models.DO_NOTHING)

    def __str__(self) -> str:
        return self.nome

class DisciplinasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplinas
        fields = "__all__"

class Temas(models.Model):
    tema = models.CharField(max_length = 100)
    disciplina = models.ForeignKey(Disciplinas, on_delete = models.DO_NOTHING)

    def __str__(self) -> str:
        return self.tema

class Aulas(models.Model):
    nome = models.CharField(max_length = 100)
    tema = models.ForeignKey(Temas, on_delete = models.DO_NOTHING, blank=True)
    aula = models.FileField(upload_to = "aulas", blank=True)
    mapa = models.ImageField(upload_to = "mapa_Aula")

    def __str__(self) -> str:
        return self.nome

class AulasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aulas
        fields = "__all__"

class TemasSerializer(serializers.ModelSerializer):
    aulas = serializers.SerializerMethodField()

    class Meta:
        model = Temas
        fields = "__all__"

    def get_aulas(self, obj):
        aulas = Aulas.objects.filter(tema=obj)
        return AulasSerializer(aulas, many=True).data

class MapasTexto(models.Model):
    aula = models.OneToOneField(Aulas, on_delete = models.CASCADE, null=True)
    texto = models.CharField(max_length=500)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)

    def __str__(self):
        return self.texto

class MapasTextosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapasTexto
        fields = "__all__"

class Avaliacoe(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    aula = models.ForeignKey(Aulas, on_delete = models.CASCADE)
    nota = models.IntegerField()

    def __str__(self) -> str:
        return self.usuario.username

class AvaliacoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacoe
        fields = "__all__"

class UltimaSessao(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    aula = models.ForeignKey(Aulas, on_delete = models.DO_NOTHING)

class UltimaSessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UltimaSessao
        fields = "__all__"
