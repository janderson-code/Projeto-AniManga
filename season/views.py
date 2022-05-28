from django.shortcuts import render


def listar_season(request):
    return render(request, 'season/listar-season.html')


def editar_season(request, id):
    return render(request, 'season/editar-season.html')


def cadastrar_season(request):
    return render(request, 'season/cadastrar-season.html')


def deletar_season(request, id):
    return render(request, 'season/deletar-season.html')
