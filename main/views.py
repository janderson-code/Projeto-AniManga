import re
from django.shortcuts import render, redirect
from .forms import NewUserForm, AuthenticationFormCustom
from django.contrib.auth import login as user_login, authenticate, logout as user_logout  # add this
import requests
import random


def home(request):
	return render(request, 'home.html', {
		'animes': {
			'most_popular': popular_titles(5, "anime"),
			'not_release': future_release_titles(4, "anime")
		},
		'mangas': {
			'best_rating': best_rating_titles(4, "manga")
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


def get_title_image(images, imageType, desiredSize):

	imagesSize = ['large', 'original', 'medium', 'tiny']
	if imageType == 'cover':
		imagesTypes = ['coverImage', 'posterImage']
	elif imageType == 'poster':
		imagesTypes = ['posterImage', 'coverImage']

	for imageType in imagesTypes:
		if not images[imageType]:
			continue
		if images[imageType][desiredSize]:
			return images[imageType][desiredSize]
		for imageSize in imagesSize:
			if imagesSize == desiredSize or not images[imageType][imageSize]:
				continue
			return images[imageType][imageSize]


def get_base_title(attr):
	title = {
		'name': attr['canonicalTitle'],
		'synopsis': attr['synopsis'],
		'coverImage':  get_title_image(attr, 'cover', 'large'),
		'posterImage': get_title_image(attr, 'poster', 'medium'),
		'abbreviatedTitles': attr['abbreviatedTitles'],
		'averageRating': attr['averageRating'],
	}
	return title


def get_anime(data):
	attr = data['attributes']
	anime = get_base_title(attr)
	anime['episodeCount'] = attr['episodeCount']
	return anime


def get_manga(data):
	attr = data['attributes']
	manga = get_base_title(attr)
	manga["chapterCount"] = attr['chapterCount']
	return manga


def get_random_title(titles, total):
	return random.sample(titles, total)

# Will create a url and request -> https://kitsu.io/api/edge/anime?sort=-userCount&page[limit]=20


def request(type, parameters):
	url = "https://kitsu.io/api/edge/{0}?".format(type)
	for i, (key, value) in enumerate(parameters.items()):
		url += "{0}={1}".format(key, value)
		if i < len(parameters)-1:
			url += "&"
	print(url)
	return requests.get(url).json()


def popular_titles(total, type, offset=30):
	response = request(type, {
		'sort': '-userCount', 'page[limit]': total, 'page[offset]': random.randint(0, offset)})
	titles = []
	for data in response['data']:
		titles.append(get_anime(data) if type == 'anime' else get_manga(data))
	return get_random_title(titles, total)


def future_release_titles(total, type, offset=30):
	response = request(type, {
		'sort': '-startDate', 'page[limit]': total, 'page[offset]': random.randint(0, offset)})
	titles = []
	for data in response['data']:
		titles.append(get_anime(data) if type == 'anime' else get_manga(data))
	return get_random_title(titles, total)


def best_rating_titles(total, type, offset=50):
	response = request(type, {
		'sort': 'ratingRank', 'page[limit]': total, 'page[offset]': random.randint(0, offset)})
	titles = []
	for data in response['data']:
		titles.append(get_anime(data) if type == 'anime' else get_manga(data))
	return get_random_title(titles, total)
