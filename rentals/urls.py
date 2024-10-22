from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('movie/', views.manage_movies, name='manage_movies'),
    path('rent/', views.rent_return, name='rent_return'),
    path('dbUser/', views.db_user, name='db_user'),
    path('dbMovie/', views.db_movie, name='db_movie'),
    path('dbRent/', views.db_rent, name='db_rent'),
]
