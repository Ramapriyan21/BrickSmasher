from django.shortcuts import render

def home(request):
    return render(request, 'rentals/home.html')
from django.shortcuts import render
from .models import User

def account(request):
    context = {}
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            context['error'] = 'Email already exists.'
        else:
            User.objects.create(first_name=first_name, last_name=last_name, email=email)
            context['success'] = 'Account created successfully.'
    return render(request, 'rentals/account.html', context)
from django.shortcuts import render
from .models import Movie

def manage_movies(request):
    context = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'new':
            title = request.POST.get('title').strip()
            if title and not Movie.objects.filter(title=title).exists():
                Movie.objects.create(title=title, stock=1)
            else:
                context['error'] = 'Invalid title or movie already exists.'
        elif action in ['add', 'remove']:
            movie_id = request.POST.get('movie_id')
            try:
                movie = Movie.objects.get(id=movie_id)
                if action == 'add':
                    movie.stock += 1
                elif action == 'remove' and movie.stock > 0:
                    movie.stock -= 1
                movie.save()
            except Movie.DoesNotExist:
                context['error'] = 'Invalid movie ID.'
    context['movies'] = Movie.objects.all().order_by('title')
    return render(request, 'rentals/manage_movies.html', context)
from django.shortcuts import render
from .models import User, Movie, Checkout

def rent_return(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            context['user'] = user
            context['checked_out_movies'] = user.checkout_set.all()
            context['available_movies'] = Movie.objects.filter(stock__gt=0)
        except User.DoesNotExist:
            context['error'] = 'User not found.'
    return render(request, 'rentals/rent_return.html', context)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def db_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists.'}, status=400)
        else:
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email)
            return JsonResponse({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
    elif request.method == 'GET':
        email = request.GET.get('email')
        try:
            user = User.objects.get(email=email)
            return JsonResponse({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
@csrf_exempt
def db_movie(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        if action == 'new':
            title = data.get('title').strip()
            if title and not Movie.objects.filter(title=title).exists():
                Movie.objects.create(title=title, stock=1)
                movies = list(Movie.objects.values())
                return JsonResponse(movies, safe=False)
            else:
                return JsonResponse({'error': 'Invalid title or movie already exists.'}, status=400)
        elif action in ['add', 'remove']:
            movie_id = data.get('movie_id')
            try:
                movie = Movie.objects.get(id=movie_id)
                if action == 'add':
                    movie.stock += 1
                elif action == 'remove' and movie.stock > 0:
                    movie.stock -= 1
                movie.save()
                movies = list(Movie.objects.values())
                return JsonResponse(movies, safe=False)
            except Movie.DoesNotExist:
                return JsonResponse({'error': 'Invalid movie ID.'}, status=404)
    elif request.method == 'GET':
        movies = list(Movie.objects.values())
        return JsonResponse(movies, safe=False)
@csrf_exempt
def db_rent(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        movie_id = data.get('movie_id')
        action = data.get('action')
        try:
            user = User.objects.get(id=user_id)
            movie = Movie.objects.get(id=movie_id)
            if action == 'rent':
                if Checkout.objects.filter(user=user, movie=movie).exists():
                    return JsonResponse({'error': 'Movie already checked out by user.'}, status=400)
                if Checkout.objects.filter(user=user).count() >= 3:
                    return JsonResponse({'error': 'User cannot check out more than 3 movies.'}, status=400)
                if movie.stock == 0:
                    return JsonResponse({'error': 'No copies of movie in stock.'}, status=400)
                Checkout.objects.create(user=user, movie=movie)
                movie.stock -= 1
                movie.save()
            elif action == 'return':
                checkout = Checkout.objects.get(user=user, movie=movie)
                checkout.delete()
                movie.stock += 1
                movie.save()
            checkouts = list(Checkout.objects.filter(user=user).values())
            return JsonResponse(checkouts, safe=False)
        except (User.DoesNotExist, Movie.DoesNotExist, Checkout.DoesNotExist):
            return JsonResponse({'error': 'Invalid user ID or movie ID.'}, status=404)
    elif request.method == 'GET':
        user_id = request.GET.get('user_id')
        movie_id = request.GET.get('movie_id')
        if user_id and movie_id:
            checkouts = list(Checkout.objects.filter(user_id=user_id, movie_id=movie_id).values())
        elif user_id:
            checkouts = list(Checkout.objects.filter(user_id=user_id).values())
        elif movie_id:
            checkouts = list(Checkout.objects.filter(movie_id=movie_id).values())
        else:
            checkouts = list(Checkout.objects.values())
        return JsonResponse(checkouts, safe=False)
