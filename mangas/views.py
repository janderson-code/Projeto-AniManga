import json
import zipfile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from yaml import serialize
from .forms import NewMangaForm
from .models import Manga
from django.core import serializers
from django.http import JsonResponse


def listar_mangas(request):
    return render(request, 'mangas/listar-mangas.html', {'mangas': Manga.objects.all(),'current_user': request.user})

def json_body(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return body

def editar_manga(request, id):
    def get():
        manga = Manga.objects.get(id=id)
        form = NewMangaForm(instance=manga)
        return render(request, 'mangas/editar-manga.html', {'new_manga_form': form})

    def post():
        manga = Manga.objects.get(id=id)
        form = NewMangaForm(request.POST, instance=manga)
        if form.is_valid():
            form.save()
            return redirect('listar_mangas')
    if request.method == 'POST':
        return post()
    return get()


def cadastro_auto_complete(request):
    def post():
        def auto_complete(search_term):
            from animanga import kitsu_api
            import re
            id = None
            if re.match(r"^\d+$", search_term):
                id = search_term
            elif re.match(r"^https://kitsu.io/manga/\d+$", search_term):
                id = re.findall(r"\d+", search_term)[0]
            if id is not None:
                manga = kitsu_api.search_by("manga",id=id,details=True)
                return json.dumps(manga)
            manga = kitsu_api.search_by("manga",name=search_term,details=True)
            return json.dumps(manga)

        content = json_body(request)
        kitsu_link = content['kitsuLink']
        if not kitsu_link:
            redirect('cadastrar_manga')
        return JsonResponse(auto_complete(kitsu_link), safe=False)
    if request.method == 'POST':
        return post()
    return redirect('listar_mangas')

def cadastrar_manga(request):
    def get():
        return render(request, 'mangas/cadastrar-manga.html', {'new_manga_form': NewMangaForm()})

    def post():
        form = NewMangaForm(request.POST)
        if not form.is_valid():
            return render(request, "mangas/cadastrar-manga.html", {'new_manga_form': form})
        manga = form.cleaned_data
        Manga.objects.create(
            title=manga['title'],
            description=manga['description'],
            status=manga['status'],
            total_chapters=manga['total_chapters'],
            official_thumbnail=manga['official_thumbnail'],
            custom_thumbnail=manga['custom_thumbnail'],
            author=manga['author'],
            kitsu_link=manga['kitsu_link'],
            user_id=request.user
        )
        return redirect('listar_mangas')
    if request.method == "POST":
        return post()
    return get()


def deletar_manga(request, id):
    Manga.objects.get(id=id).delete()
    return redirect('listar_mangas')


def download(request):
    """Download archive zip file of code snippets"""
    response = HttpResponse(content_type='application/zip')
    zf = zipfile.ZipFile(response, 'w')
    # create the zipfile in memory using writestr
    # add a readme
    zf.writestr(README_NAME, README_CONTENT)

    # retrieve snippets from ORM and them to zipfile
    mangas = Manga.objects.all()
    mangasJson = serializers.serialize('json', mangas)
    zf.writestr("tabelaManga.json", mangasJson)

    # return as zipfile
    response['Content-Disposition'] = f'attachment; filename={ZIPFILE_NAME}'
    return response


README_NAME = 'README.md'
README_CONTENT = """
## Janderson e Lucas criadores

Este arquivo zip contém os dados da tabela mangá
do projeto Animangá em formato Json
"""
ZIPFILE_NAME = 'TabelaManga.zip'
