import requests

def list_categories():
    listOfCategories = requests.get("https://www.themealdb.com/api/json/v1/1/categories.php").json()
    categories = []
    for f in range(len(listOfCategories["categories"])):
        categories.append(listOfCategories["categories"][f]['strCategory'])
    return categories

def filterByCategory(category:str):
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
    response = requests.get(url).json()
    output = []
    
    if response and response.get("meals"):
        for meal in response["meals"]:
            output.append(meal)
    
    return output

def filterByMainIngredient(mainIngredient:str):
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={mainIngredient}"


def searchByName(name:str):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={name}"
    response = requests.get(url).json()
    return response

def searchByMealId(meal_id:str):
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    response = requests.get(url).json()
    return response

