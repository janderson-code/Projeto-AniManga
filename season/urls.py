from django.urls import path

from . import views

urlpatterns = [
    path('', views.listar_season, name='listar_season'),
    path('cadastrar-season/', views.cadastrar_season, name='cadastrar_season'),
    path('editar-season/<int:id>/', views.editar_season, name='editar_season'),
    path('deletar-season/<int:id>/', views.deletar_season, name='deletar_season'),
]
