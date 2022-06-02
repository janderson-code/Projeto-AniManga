import zipfile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewSeasonForm
from .models import Season
from django.core import serializers


def listar_season(request):
    seasons = Season.objects.all()
    for season in seasons:
        if season.season_name == 'Outono':
            season.image = 'season-autumn.jpg'
        elif season.season_name == 'Inverno':
            season.image = 'season-winter.jpg'
        elif season.season_name == 'Primavera':
            season.image = 'season-spring.jpg'
        elif season.season_name == 'Verão':
            season.image = 'season-summer.jpg'

    return render(request, 'season/listar-season.html', {'seasons': seasons})


def editar_season(request, id):
    def get():
        season = Season.objects.get(id=id)
        form = NewSeasonForm(instance=season)
        return render(request, 'season/editar-season.html', {'new_season_form': form})

    def post():
        season = Season.objects.get(id=id)
        form = NewSeasonForm(request.POST, instance=season)
        if not form.is_valid():
            return render(request, "season/editar-season.html", {'new_season_form': form})
        form.save()
        return redirect('listar_season')
    if request.method == "POST":
        return post()
    return get()


def cadastrar_season(request):
    def get():
        return render(request, 'season/cadastrar-season.html', {'new_season_form': NewSeasonForm()})

    def post():
        form = NewSeasonForm(request.POST)
        if not form.is_valid():
            return render(request, "season/cadastrar-season.html", {'new_season_form': form})
        season = form.cleaned_data
        Season.objects.create(**season)
        return redirect('listar_season')
    if request.method == "POST":
        return post()
    return get()


def deletar_season(request, id):
    print(f"Id: {id}")
    Season.objects.get(id=id).delete()
    return redirect('listar_season')


def download(request):
    """Download archive zip file of code snippets"""
    response = HttpResponse(content_type='application/zip')
    zf = zipfile.ZipFile(response, 'w')
    # create the zipfile in memory using writestr
    # add a readme
    zf.writestr(README_NAME, README_CONTENT)

    # retrieve snippets from ORM and them to zipfile
    season = Season.objects.all()
    seasonJson = serializers.serialize('json', season)
    for season in season:
        zf.writestr("tabelaSeason", seasonJson)

    # return as zipfile
    response['Content-Disposition'] = f'attachment; filename={ZIPFILE_NAME}'
    return response


README_NAME = 'README.md'
README_CONTENT = """
## Janderson e Lucas criadores

Este arquivo zip contém os dados da tabela Season
do projeto Animangá em formato Json
"""
ZIPFILE_NAME = 'TabelaSeason.zip'
