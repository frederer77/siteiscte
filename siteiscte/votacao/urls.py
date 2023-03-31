from django.urls import include, path
from . import views


# (. significa que importa views da mesma directoria)
app_name = 'votacao'
urlpatterns = [
    # ex: votacao/
    path("", views.index, name='index'),

    # ex: votacao/1
    path('<int:questao_id>', views.detalhe, name='detalhe'),

    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados, name='resultados'),

    # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto, name='voto'),

    # ex: votacao/criar
    path('criar', views.criarquestao, name='criarquestao'),

    # ex: votacao/eliinar
    path('eliminar', views.eliminarQuestao, name='eliminarQuestao'),

    path('eliminar/eliminarQuestao',
         views.eliminar, name='eliminar'),
    # ex: votacao/1/criaropcao
    path('<int:questao_id>/criaropcao',
         views.criaropcao, name='criaropcao'),

    path('<int:questao_id>/save_option', views.save_option, name='save_option'),

    path('<int:opcao_id>/eliminarOpcao',
         views.eliminarOpcao, name='eliminarOpcao'),

    path('criarAluno', views.criarAluno, name='criarAluno'),

    # ex: /
    path('votacao/login', views.loginview, name='login'),

    # ex: /
    path('logout', views.logoutview, name='logout'),

    # ex: /
    path('detalheAluno', views.detalheAluno, name='detalheAluno'),

]
