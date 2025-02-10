from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import Informacoes, InformacoesSerializer, UserSerializer, CadastroSerializer, LoginSerializer, InformacaoSerializer

# LoginView
class LoginView(ObtainAuthToken):
    @swagger_auto_schema(
        responses={200: LoginSerializer(many=False)},
        operation_description="Retorna token e usuário."
    )  
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        try:
          token, _created = Token.objects.get_or_create(user=user)
        except Exception as e:
          return Response({"response": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if user:
          token, _created = Token.objects.get_or_create(user=user)
          return Response({
            'user_id': user.pk,
            'token': token.key,
        })
        else:          
          return Response({"error": "Credenciais inválidas"}, status=400)


# CadastroView
class CadastroView(APIView):
    permission_classes = [AllowAny] 
  
    @swagger_auto_schema(
        request_body=CadastroSerializer(many=False),
        operation_description="Cadastra Usuário."
    )
    def post(self, request):
        serializer = CadastroSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            # Criação do usuário
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['senha']  # Certifique-se de que o campo é 'password' no serializer
            )

            # Criação das informações adicionais
            Informacoes.objects.create(
                usuario=user,
                escolaridade=data['escolaridade'],
                vestibulares=data['vestibulares'],
                curso=data['curso'],
                universidade=data['universidade']
            )

            return Response({"response": "Usuário cadastrado com sucesso"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"response": "Erro ao salvar os dados"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# InformacoesViewSet
class InformacoesViewSet(ModelViewSet):
    queryset = Informacoes.objects.all()
    serializer_class = InformacoesSerializer    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={200: InformacaoSerializer(many=False)},
        operation_description="Retorna as informações do usuário."
    )  
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        try:
            informacoes = Informacoes.objects.get(usuario=user)
        except User.DoesNotExist:
            raise Http404("Usuário não encontrado")
        except Informacoes.DoesNotExist:
            raise Http404("Informações do usuário não encontradas")
          
        # Serializar os dados
        user_data = UserSerializer(user).data
        
        informacoes_data = self.get_serializer(informacoes).data 
        informacoes_data.pop("usuario", None)

        # Unindo os dicionários
        response_data = {**user_data, **informacoes_data}
        
        return Response(response_data)
