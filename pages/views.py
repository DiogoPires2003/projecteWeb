"""Views for visual-only pages."""
from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def login(request):
    return render(request, "pages/login.html")


def settings(request):
    return render(request, "pages/settings.html")


def ingredient_info(request):
    return render(request, "pages/ingredient-info.html")


def recipe_info(request):
    return render(request, "pages/recipe-info.html")


def ingredients(request):
    return render(request, "pages/ingredients.html")


def recipes(request):
    return render(request, "pages/recipes.html")
