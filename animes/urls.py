from django.urls import path

from . import views

urlpatterns = [
    path('', views.listar_animes),
    path('cadastrar-anime/', views.cadastrar_anime, name='cadastrar_anime'),
    path('editar-anime/<int:id>/', views.editar_anime, name='editar_anime'),
    path('deletar-anime/<int:id>/', views.deletar_anime, name='deletar_anime'),
    
]
