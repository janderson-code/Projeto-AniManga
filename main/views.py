import re
from django.shortcuts import render, redirect
from .forms import NewUserForm, AuthenticationFormCustom
from django.contrib.auth import login as user_login, authenticate, logout as user_logout  # add this
from animanga import kitsu_api
import random


def home(request):


	return render(request, 'home.html', {
		'animes': {
			'most_popular': kitsu_api.popular_titles(5, "anime",random=True),
			'not_release': kitsu_api.future_release_titles(4, "anime",random=True)
		},
		'mangas': {
			'best_rating': kitsu_api.best_rating_titles(4, "manga",random=True)
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
