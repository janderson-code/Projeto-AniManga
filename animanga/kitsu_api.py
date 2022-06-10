import requests
import random as ra

# Create a url and request -> https://kitsu.io/api/edge/anime?sort=-userCount&page[limit]=20


def request(type, parameters={},base_url=''):
    if  not base_url:
        base_url = f'https://kitsu.io/api/edge/{type}?'
    for i, (key, value) in enumerate(parameters.items()):
        base_url += "{0}={1}".format(key, value)
        if i < len(parameters)-1:
            base_url += "&"
    print(base_url)
    return requests.get(base_url).json()

def search_by(type,name=None, id=None, details=False):
    if name is None and id is None:
        raise ValueError('name or id must be provided')
    parameter_filter =  {'filter[text]': name} if name else {'filter[id]': id}
    response = request(type,parameter_filter)
    if type == 'anime':
        return get_anime(response['data'][0],details)
    return get_manga(response['data'][0],details)

def get_random_title(titles, total):
    print(len(titles))
    print(total)
    return ra.sample(titles, total)

def get_base_title(attr):
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
    title = {
        'name': attr['canonicalTitle'],
        'synopsis': attr['synopsis'],
        'coverImage':  get_title_image(attr, 'cover', 'large'),
        'posterImage': get_title_image(attr, 'poster', 'medium'),
        'abbreviatedTitles': attr['abbreviatedTitles'],
        'averageRating': attr['averageRating'],
    }
    return title

def get_productions(type,rel,role):
    productions = request(type,base_url=rel['productions']['links']['related'])['data']
    for production in productions:
        if production['attributes']['role'] == role:
           company = request(type,base_url=production['relationships']['company']['links']['related'])
           return company['data']['attributes']['name']
    raise ValueError(f'Role {role} not found')

def get_staff(type,rel,role):
    staffs = request(type,base_url=rel['staff']['links']['related'])['data']
    for staff in staffs:
        if staff['attributes']['role'] == role:
           company = request(type,base_url=staff['relationships']['person']['links']['related'])
           return company['data']['attributes']['name']
    raise ValueError(f'Role {role} not found')

def get_anime(data,details=False):
    attr = data['attributes']
    anime = get_base_title(attr)
    anime["kitsuPage"] = f"https://kitsu.io/anime/{attr['slug'] if attr['slug'] else data['id']}"
    anime['episodeCount'] = attr['episodeCount']
    anime['subtype'] = attr['subtype']
    anime['status'] = attr['status']
    anime['startDate'] = attr['startDate']
    if details:
        try:
            anime['studio'] = get_productions('anime',data['relationships'],'studio')
        except ValueError:
            anime['studio'] = "[Estúdio não encontrado]"
    return anime


def get_manga(data,details=False):
    attr = data['attributes']
    manga = get_base_title(attr)
    manga["kitsuPage"] = f"https://kitsu.io/manga/{attr['slug'] if attr['slug'] else data['id']}"
    manga["chapterCount"] = attr['chapterCount']
    manga['subtype'] = attr['subtype']
    manga['status'] = attr['status']
    manga['startDate'] = attr['startDate']
    if details:
        try:
            manga['author'] = get_staff('manga',data['relationships'],'Story & Art')
        except ValueError:
            manga['author'] = "[Autor não encontrado]"
    return manga


def popular_titles(total, type, offset=30, random=True):
    response = request(type, parameters={
            'sort': '-userCount',
            'page[limit]': 20,
            'page[offset]':  ra.randint(0, offset) if random else offset
         })
    titles = []
    for data in response['data']:
        titles.append(get_anime(data) if type == 'anime' else get_manga(data))
    if not random:
        return titles
    return get_random_title(titles, total)


def future_release_titles(total, type, offset=30, random=True):
    response = request(type, parameters= {
        'sort': '-startDate',
        'page[limit]': 20,
        'page[offset]': ra.randint(0, offset) if random else offset
    }
    )
    titles = []
    for data in response['data']:
        titles.append(get_anime(data) if type == 'anime' else get_manga(data))
    if not random:
        return titles
    return get_random_title(titles, total)


def best_rating_titles(total, type, offset=50, random=True):
    response = request(type, parameters= {
        'sort': 'ratingRank',
        'page[limit]': 20,
        'page[offset]': ra.randint(0, offset) if random else offset
    })
    titles = []
    for data in response['data']:
        titles.append(get_anime(data) if type == 'anime' else get_manga(data))
    if not random:
        return titles
    return get_random_title(titles, total)
