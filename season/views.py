from django.shortcuts import render, redirect
from .forms import NewSeasonForm
from .models import Season

def listar_season(request):
	seasons = Season.objects.all()
	for season in  seasons:
		if season.season_name == 'Outono': season.image = 'season-autumn.jpg'
		elif season.season_name == 'Inverno': season.image = 'season-winter.jpg'
		elif season.season_name == 'Primavera': season.image = 'season-spring.jpg'
		elif season.season_name == 'Verão': season.image = 'season-summer.jpg'

	return render(request, 'season/listar-season.html', {'seasons': seasons})


def editar_season(request, id):
	def get():
		season = Season.objects.get(id=id)
		form  = NewSeasonForm(instance=season)	
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
