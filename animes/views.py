from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from season.models import Season
from .forms import NewAnimeForm
from .models import Anime
# Create your views here.

def listar_animes(request):
	return render(request, 'animes/listar-animes.html', {'animes': Anime.objects.all()})


def editar_anime(request,id):
	def default():
		anime = Anime.objects.get(id=id)
		form  = NewAnimeForm(instance=anime,initial={'seasons':anime.season,'subtype':anime.subtype})	
		return render(request, 'animes/editar-animes.html', {'new_anime_form': form})
	def post():
		anime = Anime.objects.get(id=id)
		form = NewAnimeForm(request.POST,instance=anime)
		if form.is_valid():
			anime = form.save(commit=False)
			season = form.cleaned_data['seasons']
			anime.season = season
			anime.save()
			return redirect('listar_animes')
	if request.method == 'POST':
		return post()
	return default()

def cadastrar_anime(request):
	if request.method != "POST":
		return render(request, "animes/cadastrar-anime.html", {'new_anime_form': NewAnimeForm()})
	form = NewAnimeForm(request.POST)
	if not form.is_valid():
		return render(request, "animes/cadastrar-anime.html", {'new_anime_form': form})
	anime = form.cleaned_data
	print(anime['seasons'])
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

def deletar_anime(request,id):
	Anime.objects.get(id=id).delete()
	return redirect('listar_animes')
