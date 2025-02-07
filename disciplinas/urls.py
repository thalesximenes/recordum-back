from django.urls import path, include 
from .views import EixosListView, DisciplinasListView, TemasListView, AulasDetailView, MapasTextoListView

app_name = 'disciplinas'

urlpatterns = [
    path('eixos/',
         EixosListView.as_view(), 
         name='eixos-list'),

    path('disciplinas/<int:fk>',
         DisciplinasListView.as_view(), 
         name='disciplinas detail'),

    path('temas/<int:fk>/',
         TemasListView.as_view(), 
         name='temas list'),

    path('aula/<int:pk>',
         AulasDetailView.as_view(), 
         name='aulas list disciplina'),

    path('mapastexto/<int:fk>',
         MapasTextoListView.as_view(), 
         name='mapastexto'),

    # path('disciplinas/',
    #      DisciplinasListView.as_view(), 
    #      name='disciplinas list'),

    # path('avaliacoes/<int:fk>',
    #      AvaliacoesListView.as_view(), 
    #      name='avaliacoes'),

    # path('arquivos/recuperar/<int:pk>/',
    #     arquivos_recuperar, 
    #     name='arquivos_recuperar'),

]
