import zipfile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from season.models import Season
from .forms import NewAnimeForm
from .models import Anime
from django.core import serializers


def listar_animes(request):
    return render(request, 'animes/listar-animes.html', {'animes': Anime.objects.all()})


def cadastro_auto_complete(request, id):
    def post():
        def auto_complete(search_term):
            from animanga import kitsu_api
            import re
            if re.match(r"^\d+$"):
                id = search_term
            elif re.match(r"^https://kitsu.io/anime/\d+$"):
                id = re.findall(r"\d+", search_term)[0]
            if id is not None:
                anime = kitsu_api.get_anime('anime', id=id)
                return NewAnimeForm(instance=anime)
            anime = kitsu_api.get_anime('anime', name=search_term)
            return NewAnimeForm(instance=anime)

        anime = Anime.objects.get(id=id)
        form = NewAnimeForm(request.POST, instance=anime)
        filled_anime = anime
        filled_anime.title = form.cleaned_data['title']
        form = auto_complete(form.cleaned_data['kitsu_link'])
        return render(request, 'animes/editar-animes.html', {'new_anime_form': form})


def editar_anime(request, id):
    def get():
        anime = Anime.objects.get(id=id)
        form = NewAnimeForm(instance=anime, initial={
                            'seasons': anime.season, 'subtype': anime.subtype})
        return render(request, 'animes/editar-animes.html', {'new_anime_form': form})

    def post():
        anime = Anime.objects.get(id=id)
        form = NewAnimeForm(request.POST, instance=anime)
        if form.is_valid():
            anime = form.save(commit=False)
            season = form.cleaned_data['seasons']
            anime.season = season
            anime.save()
            return redirect('listar_animes')
    if request.method == 'POST':
        return post()
    return get()


def cadastrar_anime(request):
    def get():
        return render(request, 'animes/cadastrar-anime.html', {'new_anime_form': NewAnimeForm()})

    def post():
        form = NewAnimeForm(request.POST)
        if not form.is_valid():
            return render(request, "animes/cadastrar-anime.html", {'new_anime_form': form})
        anime = form.cleaned_data
        Anime.objects.create(
            title=anime['title'],
            description=anime['description'],
            status=anime['status'],
            total_episodes=anime['total_episodes'],
            official_thumbnail=anime['official_thumbnail'],
            custom_thumbnail=anime['custom_thumbnail'],
            studio=anime['studio'],
            kitsu_link=anime['kitsu_link'],
            subtype=anime['subtype'],
            season=anime['seasons'],
            user_id=request.user
        )
        return redirect('listar_animes')

    if request.method == "POST":
        return post()
    return get()


def deletar_anime(request, id):
    Anime.objects.get(id=id).delete()
    return redirect('listar_animes')


def download(request):
    """Download archive zip file of code snippets"""
    response = HttpResponse(content_type='application/zip')
    zf = zipfile.ZipFile(response, 'w')
    # create the zipfile in memory using writestr
    # add a readme
    zf.writestr(README_NAME, README_CONTENT)

    # retrieve snippets from ORM and them to zipfile
    animes = Anime.objects.all()
    animesJson = serializers.serialize('json', animes)
    for animes in animes:
        zf.writestr("tabelaAnime", animesJson)

    # return as zipfile
    response['Content-Disposition'] = f'attachment; filename={ZIPFILE_NAME}'
    return response


README_NAME = 'README.md'
README_CONTENT = """
## PyBites Code Snippet Archive

## Janderson e Lucas criadores

Este arquivo zip contém os dados da tabela Animes
do projeto Animangá em formato Json
"""
ZIPFILE_NAME = 'tabelaAnime.zip'
