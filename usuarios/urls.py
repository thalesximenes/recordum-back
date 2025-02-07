from django.urls import path
from .views import CadastroView, LoginView, InformacoesViewSet

app_name = 'usuarios'

urlpatterns = [
    path('cadastro/',
         CadastroView.as_view(), 
         name='cadastro'),

    path('login/',
         LoginView.as_view(), 
         name='disciplinas'),

     path('informacao/',
         InformacoesViewSet.as_view({'get': 'retrieve'}), 
         name='informacao'),
         
]