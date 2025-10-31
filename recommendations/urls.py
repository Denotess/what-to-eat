from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("load-meals/", views.load_meals, name="load_meals"),
    path("meal-details/", views.meal_details, name="meal_details"),
    path("search-results/", views.search_results, name="search_results"),
    path("favorites/", views.favorites, name="favorites"),
    path("favorites/add/", views.add_favorites, name="add_favorites"),
    path("favorites/remove/", views.remove_favorites, name="remove_favorites"),
    path("autocomplete/", views.autocomplete, name="autocomplete"),

]