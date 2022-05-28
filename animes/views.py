from django.shortcuts import render

# Create your views here.

def listar_animes(request):
    return render(request, 'animes/listar-animes.html')

def editar_anime(request,id):
    return render(request, 'animes/editar-animes.html')

def cadastrar_anime(request):
    return render(request, 'animes/cadastrar-anime.html')

def deletar_anime(request,id):
    return render(request, 'animes/deletar-anime.html')