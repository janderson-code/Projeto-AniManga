from django.shortcuts import render, redirect
from season.models import Season
from .forms import NewAnimeForm
from .models import Anime

def listar_animes(request):
	return render(request, 'animes/listar-animes.html', {'animes': Anime.objects.all()})


def editar_anime(request,id):
	def get():
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
		post()
	return get()

def deletar_anime(request,id):
	Anime.objects.get(id=id).delete()
	return redirect('listar_animes')
