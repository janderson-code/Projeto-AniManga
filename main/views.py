from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewUserForm, AuthenticationFormCustom
from django.contrib.auth import login as user_login, authenticate, logout as user_logout  # add this
from django.contrib import messages
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

    def auth_user(form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        return authenticate(username=username, password=password)
    if request.user.is_authenticated:
        return redirect('home')
    if request.method != "POST":
        return render(request, "login.html", {'login_form': AuthenticationFormCustom()})
    form = AuthenticationFormCustom(request, data=request.POST)
    if not form.is_valid():
        print(form)
        messages.error(request, "Usuário ou senha incorretos.")
        return render(request, "login.html", {'login_form': form})
    user = auth_user(form)
    if user is not None:
        user_login(request, user)
        return redirect("home")
    else:
        return render(request, "login.html", {"login_form": form})


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Ative sua conta'
            message = render_to_string('website/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user=user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Por favor confirme seu email para prosseguir com o registro da sua conta')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
    else:
        print('in else')
        form = NewUserForm()
    return render(request, "register.html", {'register_form': NewUserForm()})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Sua conta foi ativada com sucesso')
    else:
        return HttpResponse('Link de ativação é invalido!')


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
