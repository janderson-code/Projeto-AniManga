from django.shortcuts import render
import requests
import random

def home(request):
    return render(request, 'animanga/home.html', {
        'animes':{
            'most_popular': popular_titles(5,"anime"),
            'not_release': future_release_titles(4,"anime")
        },
        'mangas':{
            'best_rating': best_rating_titles(4,"manga")
        }       
        })


def get_title_image(images,imageType,desiredSize):
    
    imagesSize = ['large','original','medium','tiny']
    if imageType == 'cover': imagesTypes = ['coverImage','posterImage']      
    elif imageType == 'poster': imagesTypes = ['posterImage','coverImage']

    for imageType in imagesTypes:
        if not images[imageType]: continue
        if images[imageType][desiredSize]: return images[imageType][desiredSize]
        for imageSize in imagesSize:
            if imagesSize == desiredSize or not images[imageType][imageSize]:
                continue
            return images[imageType][imageSize]


def get_base_title(attr):
    title = {
        'name': attr['canonicalTitle'],
        'synopsis': attr['synopsis'],
        'coverImage':  get_title_image(attr,'cover', 'large'),
        'posterImage': get_title_image(attr,'poster', 'medium'),
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

def get_random_title(titles,total):
    return random.sample(titles,total)

#Will create a url and request -> https://kitsu.io/api/edge/anime?sort=-userCount&page[limit]=20
def request(type,parameters):
    url = "https://kitsu.io/api/edge/{0}?".format(type)
    for i,(key,value) in enumerate(parameters.items()):
        url += "{0}={1}".format(key,value)
        if i < len(parameters)-1:  url += "&"
    print(url)
    return requests.get(url).json()

def popular_titles(total,type,offset=30):
    response = request(type,{'sort':'-userCount','page[limit]':total,'page[offset]':random.randint(0,offset)})
    titles = []
    for data in response['data']: titles.append(get_anime(data) if type == 'anime' else get_manga(data))
    return get_random_title(titles,total)

def future_release_titles(total,type,offset=30):
    response = request(type,{'sort':'-startDate','page[limit]':total,'page[offset]':random.randint(0,offset)})
    titles = []
    for data in response['data']: titles.append(get_anime(data) if type == 'anime' else get_manga(data))
    return get_random_title(titles,total)

def best_rating_titles(total,type,offset=50):
    response = request(type,{'sort':'ratingRank','page[limit]':total,'page[offset]':random.randint(0,offset)})
    titles = []
    for data in response['data']: titles.append(get_anime(data) if type == 'anime' else get_manga(data))
    return get_random_title(titles,total)


    

        

    