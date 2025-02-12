from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from .models import EixosSerializer, EixosTematicos, DisciplinasSerializer, Disciplinas, TemasSerializer, Temas, AulasSerializer, Aulas, MapasTextos, MapasTextosSerializer, AvaliacoesSerializer, Avaliacoes 
from django.http import Http404

from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

class EixosListView(APIView):
    @swagger_auto_schema(
        responses={200: openapi.Response(
          description="Lista de eixos retornada com sucesso", 
          schema=EixosSerializer(many=True))
          },
        operation_description="Retorna os eixos de estudo."
    )  
    def get(self, request):
        eixos = EixosTematicos.objects.all()
        serializer = EixosSerializer(eixos, many = True)
        return Response(serializer.data)

class DisciplinasListView(APIView):
    @swagger_auto_schema(
        responses={200: openapi.Response(
          description="Lista de disciplinas retornada com sucesso",
          schema=DisciplinasSerializer(many=True))},
        operation_description="Retorna as disciplinas de acordo com um eixo temático."
    )  
    def get(self, request, fk):
        disciplinas = Disciplinas.objects.annotate(quantidade_aulas=Count('temas__aulas'))
        data = [{'id': d.id, 'nome': d.nome, 'quantidade_aulas': d.quantidade_aulas} for d in disciplinas]
        return Response(data)

class TemasListView(APIView):
    permission_classes = [AllowAny] 
    @swagger_auto_schema(
        responses={200: openapi.Response(
          description="Lista de temas retornada com sucesso",
          schema=TemasSerializer(many=True))},
        operation_description="Retorna os temas de acordo com a disciplina escolhida."
    )  
    def get(self, request, fk):
        tema = Temas.objects.filter(disciplina = fk)        
        tema_data = TemasSerializer(tema, many = True).data
        
        return Response(tema_data)

class AulasDetailView(APIView):
    @swagger_auto_schema(
        responses={200: openapi.Response(
          description="Lista de informações da aula retornada com sucesso",
          schema=AulasSerializer(many=False))},
        operation_description="Retorna as informações da aula selecionada."
    )  
    def get(self, request, pk):
        aulas = Aulas.objects.get(id = pk)
        serializer = AulasSerializer(aulas)
        return Response(serializer.data)
      
class MapasTextosListView(APIView):
    @swagger_auto_schema(
        responses={200: openapi.Response(
          description="Lista de texto dos mapas retornada com sucesso",
          schema=MapasTextosSerializer(many = True))},
        operation_description="Retorna os textos dos mapas de acordo com uma aula."
    )  
    def get(self, request, fk):
        mapas = MapasTextos.objects.filter(aula = fk)
        serializer = MapasTextosSerializer(mapas, many = True)
        return Response(serializer.data)


class AvaliacoesListView(APIView):
    def get_avaliacoes(self, fk):
        try:
            return Avaliacoes.objects.filter(aula = fk)
        except Avaliacoes.DoesNotExist:
            raise Http404

    def get(self, request, fk):
        avaliacoes = self.get_avaliacoes(fk)
        serializer = AvaliacoesSerializer(avaliacoes, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        avaliacao_serializer = AvaliacoesSerializer(data = request.data)
        if avaliacao_serializer.is_valid():
            avaliacao_serializer.save()
            return Response(avaliacao_serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(avaliacao_serializer.errors) 
