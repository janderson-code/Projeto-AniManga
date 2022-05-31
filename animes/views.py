from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import NewAnimeForm
from .models import Anime
from .models import Season
# Create your views here.

def listar_animes(request):
	return render(request, 'animes/listar-animes.html')

def editar_anime(request,id):
	return render(request, 'animes/editar-animes.html')

def cadastrar_anime(request):
	if request.method != "POST":
		return render(request, "animes/cadastrar-anime.html", {'new_anime_form': NewAnimeForm()})
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
		season_id=anime['seasons'],
		user_id=request.user
	)

	return redirect('listar_animes')

def deletar_anime(request,id):
	return render(request, 'animes/deletar-anime.html')