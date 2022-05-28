from django.shortcuts import render
import requests
import random

def home(request):
    api = "https://kitsu.io/api/edge/anime?page[limit]=20"
    response = requests.get(api).json()
    data = response['data'][0]['attributes']['coverImage']['original']

    return render(request, 'animanga/home.html', {
        'popular_animes': popular_titles(5,"anime"),
        'future_release_animes': future_release_titles(5,"anime"),
        'best_mangas': best_rating_titles(4,"manga")
        })



def get_anime(data):
    attr = data['attributes']
    anime = {
        'title': attr['canonicalTitle'],
        'synopsis': attr['synopsis'],
        'coverImage':  attr['coverImage']['large'] if attr['coverImage'] else attr['posterImage']['original'],
        'posterImage': attr['posterImage']['medium'] if attr['posterImage'] else attr['coverImage']['medium'],
        'episodeCount': attr['episodeCount'],
        'abbreviatedTitles': attr['abbreviatedTitles'],
        'averageRating': attr['averageRating'],
    }
    return anime
def get_manga(data):
    attr = data['attributes']
    manga = {
        'title': attr['canonicalTitle'],
        'synopsis': attr['synopsis'],
        'coverImage':  attr['coverImage']['large'] if attr['coverImage'] else attr['posterImage']['medium'],
        'posterImage': attr['posterImage']['medium'] if attr['posterImage'] else attr['coverImage']['medium'],
        'abbreviatedTitles': attr['abbreviatedTitles'],
        'averageRating': attr['averageRating'],
    }
    return manga

def get_random_title(titles,total):
    return random.sample(titles,total)

def popular_titles(total,title,page_size=20):
    if total > page_size: total = page_size
    url = "https://kitsu.io/api/edge/{0}?sort=-userCount&page[limit]={1}".format(title,page_size)
    response = requests.get(url).json()
    titles = []
    for data in response['data']: titles.append(get_anime(data) if title == 'anime' else get_manga(data))
    return get_random_title(titles,total)

def future_release_titles(total,title,page_size=20):
    if total > page_size: total = page_size
    url = "https://kitsu.io/api/edge/{0}?sort=-startDate&page[limit]={1}".format(title,page_size)
    response = requests.get(url).json()
    titles = []
    for data in response['data']: titles.append(get_anime(data) if title == 'anime' else get_manga(data))
    return get_random_title(titles,total)

def best_rating_titles(total,title,page_size=20):
    if total > page_size: total = page_size
    url = "https://kitsu.io/api/edge/{0}?sort=ratingRank&page[limit]={1}".format(title,page_size)
    response = requests.get(url).json()
    titles = []
    for data in response['data']: titles.append(get_anime(data) if title == 'anime' else get_manga(data))
    return get_random_title(titles,total)


    

        

    