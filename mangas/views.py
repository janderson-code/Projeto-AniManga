from django.shortcuts import render



def listar_mangas(request):
    return render(request, 'mangas/listar-mangas.html')

def editar_manga(request, id):
    return render(request, 'mangas/editar-manga.html')

def cadastrar_manga(request):
    return render(request, 'mangas/cadastrar-manga.html')


def deletar_manga(request, id):
    return render(request, 'mangas/deletar-manga.html')