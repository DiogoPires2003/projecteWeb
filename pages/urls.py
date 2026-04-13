"""URL routes for visual-only pages."""
from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("settings/", views.settings, name="settings"),
    path("ingredient/", views.ingredient_info, name="ingredient_info"),
    path("recipe/", views.recipe_info, name="recipe_info"),
    path("ingredients/", views.ingredients, name="ingredients"),
    path("recipes/", views.recipes, name="recipes"),
]
