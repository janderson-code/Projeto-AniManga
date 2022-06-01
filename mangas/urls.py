from django.urls import path

from . import views

urlpatterns = [
    path('', views.listar_mangas,name='listar_mangas'),
    path('cadastrar-manga/', views.cadastrar_manga, name='cadastrar_manga'),
    path('editar-manga/<int:id>/', views.editar_manga, name='editar_manga'),
    path('deletar-manga/<int:id>/', views.deletar_manga, name='delete_manga'),
    
]
