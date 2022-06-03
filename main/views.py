from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
from animes.models import Anime
from .forms import NewUserForm, AuthenticationFormCustom
from django.contrib.auth import login as user_login, authenticate, logout as user_logout  # add this
import zipfile
from animanga import kitsu_api as kitsu


def home(request):
    return render(request, 'home.html', {
        'animes': {
            'most_popular': kitsu.popular_titles(5, "anime"),
            'not_release': kitsu.best_rating_titles(4, "anime")
        },
        'mangas': {
            'best_rating': kitsu.best_rating_titles(4, "manga")
        }
    })


def login(request):

    def get():
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, "login.html", {'login_form': AuthenticationFormCustom()})

    def post():
        form = AuthenticationFormCustom(request, data=request.POST)
        if not form.is_valid():
            return render(request, "login.html", {'login_form': form})
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'))
        if user is None:
            return render(request, "login.html", {"login_form": form})
        user_login(request, user)
        return redirect("home")

    if request.method == "POST":
        return post()
    return get()


def register(request):

    def get():
        return render(request, "register.html", {'register_form': NewUserForm()})

    def post():
        form = NewUserForm(request.POST)
        if not form.is_valid():
            return render(request, "register.html", {'register_form': form})
        user = form.save()
        user_login(request, user)
        return redirect("home")
    if request.method == "POST":
        return post()
    return get()


def logout(request):
    user_logout(request)
    return redirect('login')

def sobre_desenvolvedores(request):
    return render(request, 'sobre-desenvolvedores.html')

def sobre_projeto(request):
    return render(request, 'sobre-projeto.html')


def some_view(request):
    qs = Anime.objects.all()


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
    zf.writestr("tabelaAnime.json", animesJson)

    # return as zipfile
    response['Content-Disposition'] = f'attachment; filename={ZIPFILE_NAME}'
    return response


README_NAME = 'README.md'
README_CONTENT = """
## PyBites Code Snippet Archive

Here is a zipfile with some useful code snippets.

Produced for blog post https://pybit.es/django-zipfiles.html

Keep calm and code in Python!
"""
ZIPFILE_NAME = 'tabelaAnimeZipada.zip'
