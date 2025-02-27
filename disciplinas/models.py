from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class EixosTematicos(models.Model):
    nome = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.nome
    
    class Meta:
      verbose_name_plural = "Eixos Temáticos"

class EixosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EixosTematicos
        fields="__all__"

class Disciplinas(models.Model):
    nome = models.CharField(max_length = 100)
    thumb = models.CharField(max_length= 500)
    eixo = models.ForeignKey(EixosTematicos, on_delete = models.DO_NOTHING)

    def __str__(self) -> str:
        return self.nome
      
    class Meta:
      verbose_name_plural = "Disciplinas"

class DisciplinasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplinas
        fields = "__all__"

class Temas(models.Model):
    tema = models.CharField(max_length = 100)
    disciplina = models.ForeignKey(Disciplinas, on_delete = models.DO_NOTHING)

    def __str__(self) -> str:
        return self.tema

    class Meta:
      verbose_name_plural = "Temas"

class Aulas(models.Model):
    nome = models.CharField(max_length = 100)
    tema = models.ForeignKey(Temas, on_delete = models.DO_NOTHING, blank=True)
    aula = models.CharField()
    mapa = models.ImageField(upload_to = "mapa_aula")
    duracao = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.nome
      
    class Meta:
      verbose_name_plural = "Aulas"

class AulasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aulas
        fields = ("id", "nome", "aula", "mapa", "duracao")

class TemasSerializer(serializers.ModelSerializer):
    aulas = serializers.SerializerMethodField()

    class Meta:
        model = Temas
        fields = "__all__"

    def get_aulas(self, obj):
        aulas = Aulas.objects.filter(tema=obj)
        return AulasSerializer(aulas, many=True).data

class MapasTextos(models.Model):
    aula = models.ForeignKey(Aulas, on_delete = models.CASCADE, null=True)
    texto = models.CharField(max_length=500)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)

    def __str__(self):
        return self.texto

    class Meta:
      verbose_name_plural = "Mapas Textos"

class MapasTextosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapasTextos
        fields = "__all__"

class Avaliacoes(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    aula = models.ForeignKey(Aulas, on_delete = models.CASCADE)
    nota = models.IntegerField()

    def __str__(self) -> str:
        return self.usuario.username

class AvaliacoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacoes
        fields = "__all__"

class UltimaSessao(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    aula = models.ForeignKey(Aulas, on_delete = models.DO_NOTHING)

class UltimaSessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UltimaSessao
        fields = "__all__"

class NotasCornell(models.Model):
    aula = models.ForeignKey(Aulas, on_delete = models.CASCADE)
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    sumario = models.CharField(null=True)
    
class NotasCornellTopico(models.Model):
    nota = models.ForeignKey(NotasCornell, on_delete = models.CASCADE)
    topico = models.CharField()
    cor = models.CharField()

class NotasCornellAnotacao(models.Model):
    nota = models.ForeignKey(NotasCornell, on_delete = models.CASCADE)
    topico = models.ForeignKey(NotasCornellTopico, on_delete = models.DO_NOTHING, null=True)
    anotacao = models.CharField()

class NotasCornellTopicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotasCornellTopico
        fields = ['topico', 'cor']

class NotasCornellAnotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotasCornellAnotacao
        fields = ['topico', 'anotacao']