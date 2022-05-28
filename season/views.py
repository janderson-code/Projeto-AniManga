from django.shortcuts import render


def listar_season(request):
    seasons = [
        {"year": "2022","name": "Outono", "img": "season-autumn.jpg"},
        {"year": "2022", "name": "Primáveira", "img": "season-spring.jpg"},
        {"year": "2022", "name": "Verão", "img": "season-summer.jpg"},
        {"year": "2022", "name": "Inverno", "img": "season-winter.jpg"},
        {"year": "2021","name": "Outono", "img": "season-autumn.jpg"},
        {"year": "2021", "name": "Primáveira", "img": "season-spring.jpg"},
        {"year": "2021", "name": "Verão", "img": "season-summer.jpg"},
        {"year": "2021", "name": "Inverno", "img": "season-winter.jpg"},
    ]
    return render(request, 'season/listar-season.html',{"seasons": seasons})


def editar_season(request, id):
    return render(request, 'season/editar-season.html')


def cadastrar_season(request):
    return render(request, 'season/cadastrar-season.html')


def deletar_season(request, id):
    return render(request, 'season/deletar-season.html')
