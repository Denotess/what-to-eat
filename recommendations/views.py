from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .utils import list_categories, filterByCategory, searchByName, searchByMealId
from urllib.parse import urlparse, parse_qs
 


def index(request):
    categories = list_categories()
    return render(request, "index.html", {"categories":categories})

def load_meals(request):
    category = request.GET.get('categories')
    meals = filterByCategory(category)

    favorites = request.session.get('favorites', [])
    favorite_ids = [fav['id'] for fav in favorites]


    return render(request, "index.html", {
        "meals":meals,
        "is_htmx": True,
        "favorite_ids":favorite_ids
    })

def meal_details(request):
    meal_name = request.GET.get('meal')
    response = searchByName(meal_name)
    meal = response["meals"][0]

    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            ingredients.append({
                "ingredient": ingredient.strip(),
                "measure": measure.strip() if measure else ""
            })

    raw_youtube = (meal.get("strYoutube") or "").strip()
    youtube_id = ""
    if raw_youtube:
        try:
            u = urlparse(raw_youtube)
            if u.netloc.endswith("youtu.be"):
                youtube_id = u.path.lstrip("/")
            elif "youtube.com" in u.netloc:
                q = parse_qs(u.query)
                youtube_id = (q.get("v", [""])[0] or "").strip()
        except Exception:
            youtube_id = ""


    return render(request, "meal_detail.html", {"meal_name": meal_name,
                                                "id": meal["idMeal"],
                                                "name": meal["strMeal"],
                                                "category": meal["strCategory"],
                                                "area": meal["strArea"],
                                                "instructions": meal["strInstructions"],
                                                "thumbnail": meal["strMealThumb"],
                                                "tags": meal["strTags"],
                                                "youtube": meal["strYoutube"],
                                                "ingredients": ingredients,
                                                "youtube_id": youtube_id})
def search_results(request):
    search_query = request.GET.get("search", "")

    if search_query:
        response = searchByName(search_query)
        meals = response.get("meals", [])
    else:
        meals = []
    return render(request, "search_results.html", {
        "meals": meals,
        "search_query": search_query
    })

def favorites(request):
    meals = request.session.get('favorites', [])

    return render(request, 'favorites.html', {
        'meals': meals,
        'favorites_count': len(meals)
    })

def add_favorites(request):
    meal_id = request.GET.get('meal_id') 

    if not meal_id:
        return redirect('index')
    
    response = searchByMealId(meal_id)
    if not response or not response.get('meals'):
        return redirect('index')

    meal = response['meals'][0]

    favorites = request.session.get('favorites', [])


    if not any(fav['id'] == meal_id for fav in favorites):
        favorites.append({
            'id': meal['idMeal'],
            'name': meal['strMeal'],
            'thumb': meal['strMealThumb'],
            'category': meal['strCategory']
        })

    request.session['favorites'] = favorites
    return redirect(request.META.get('HTTP_REFERER', 'index'))



def remove_favorites(request):
    meal_id = request.GET.get('meal_id') 

    if not meal_id:
        return redirect('favorites')
    
    favorites = request.session.get('favorites', [])

    favorites = [fav for fav in favorites if fav['id'] != meal_id]


    request.session['favorites'] = favorites
    return redirect('favorites')

def autocomplete(request):
    query = request.GET.get('search', '').strip()

    if len(query) < 2:
        return render(request, 'autocomplete_results.html', {
            'meals': [],
            'query': query
        })

    response = searchByName(query)

    meals = response.get('meals', [])
    if meals:
        meals = meals[:5]
    else:
        meals = []
    return render(request, 'autocomplete_results.html', {'meals': meals,
                                                         'query': query})

