from django.shortcuts import render, redirect
from .forms import NewMangaForm
from .models import Manga

def listar_mangas(request):
    return render(request, 'mangas/listar-mangas.html', {'mangas': Manga.objects.all()})

def editar_manga(request,id):
	def default():
		manga = Manga.objects.get(id=id)
		form  = NewMangaForm(instance=manga)	
		return render(request, 'mangas/editar-manga.html', {'new_manga_form': form})
	def post():
		manga = Manga.objects.get(id=id)
		form = NewMangaForm(request.POST,instance=manga)
		if form.is_valid():
			form.save()
			return redirect('listar_mangas')
	if request.method == 'POST':
		return post()
	return default()

def cadastrar_manga(request):
	if request.method != "POST":
		return render(request, 'mangas/cadastrar-manga.html', {'new_manga_form': NewMangaForm()})
	form = NewMangaForm(request.POST)
	if not form.is_valid():
		return render(request, 'mangas/cadastrar-manga.html', {'new_manga_form': form})
	manga = form.cleaned_data
	Manga.objects.create(
		title=manga['title'],
		description=manga['description'],
		status=manga['status'],
		total_chapters=manga['total_chapters'],
		official_thumbnail=manga['official_thumbnail'],
		custom_thumbnail=manga['custom_thumbnail'],
		serialization=manga['serialization'],
		kitsu_link=manga['kitsu_link'],
		subtype=manga['subtype'],
		user_id=request.user
	)
	return redirect('listar_mangas')

def deletar_manga(request,id):
	Manga.objects.get(id=id).delete()
	return redirect('listar_mangas')