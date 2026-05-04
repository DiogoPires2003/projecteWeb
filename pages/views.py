from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import requests
from urllib.parse import quote
from .models import Recipe, RecipeIngredient, SavedRecipe
from .forms import (
    UserRegisterForm, RecipeForm, RecipeIngredientForm, ProfileForm
)

@login_required
def search_recipes_api(request):
    query = request.GET.get("q", "").strip()
    if not query:
        recipes = Recipe.objects.all().select_related("owner").order_by("-created_at")[:20]
    else:
        recipes = Recipe.objects.filter(title__icontains=query).select_related("owner").order_by("-created_at")[:20]
    saved_ids = set(SavedRecipe.objects.filter(user=request.user).values_list("recipe_id", flat=True))
    results = []
    for r in recipes:
        results.append({
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "image_url": r.image_url,
            "prep_time_minutes": r.prep_time_minutes,
            "difficulty": r.difficulty,
            "category": r.category,
            "ingredients_count": r.ingredients.count(),
            "owner": r.owner.username,
            "saved": r.id in saved_ids,
        })
    return JsonResponse({"results": results})

@login_required
def toggle_save_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    saved, created = SavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        saved.delete()
        return JsonResponse({"saved": False})
    return JsonResponse({"saved": True})

def home(request):
    return render(request, "pages/home.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("pages:home")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("pages:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "pages/login.html", {"form": form})

def settings(request):
    if not request.user.is_authenticated:
        return redirect("pages:login")
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    return render(request, "pages/settings.html", {
        "profile_form": profile_form,
        "password_form": password_form,
    })

@login_required
def update_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualitzat correctament.")
            return redirect("pages:settings")
        else:
            messages.error(request, "Si us plau, corregeix els errors del formulari.")
    return redirect("pages:settings")

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Contrasenya actualitzada correctament.")
            return redirect("pages:settings")
        else:
            messages.error(request, "Si us plau, corregeix els errors del formulari.")
    return redirect("pages:settings")

def ingredient_info(request):
    return render(request, "pages/ingredient-info.html")

def recipe_info(request, recipe_id=None):
    recipe = None
    if recipe_id:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, "pages/recipe-info.html", {"recipe": recipe})

def ingredients(request):
    return render(request, "pages/ingredients.html")

@login_required
def recipes(request):
    user_recipes = Recipe.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "pages/recipes.html", {"recipes": user_recipes})

def logout(request):
    auth_logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("pages:home")

def register(request):
    if request.user.is_authenticated:
        return redirect("pages:home")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome {user.username}! Registration successful.")
            return redirect("pages:home")
        else:
            messages.error(request, "Si us plau, corregeix els errors del formulari.")
    else:
        form = UserRegisterForm()
    return render(request, "pages/register.html", {"form": form})

@login_required
def create_recipe(request):
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST)
        ingredient_names = request.POST.getlist("ingredient_name")
        ingredient_quantities = request.POST.getlist("ingredient_quantity")
        ingredient_serving = request.POST.getlist("ingredient_serving")
        ingredient_codes = request.POST.getlist("ingredient_code")
        ingredient_images = request.POST.getlist("ingredient_image")
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            for name, qty, srv, code, img in zip(ingredient_names, ingredient_quantities, ingredient_serving, ingredient_codes, ingredient_images):
                if name.strip():
                    ing = RecipeIngredient.objects.create(
                        recipe=recipe,
                        name=name.strip(),
                        quantity=qty.strip(),
                        serving_qty=int(srv) if srv else 100,
                        api_code=code.strip(),
                        api_image=img.strip(),
                    )
                    if code.strip():
                        _fetch_and_save_nutrition(ing, code.strip())
            messages.success(request, "Recepta creada correctament.")
            return redirect("pages:recipes")
        else:
            messages.error(request, "Si us plau, corregeix els errors del formulari.")
            return render(request, "pages/recipe-create.html", {"recipe_form": recipe_form})
    else:
        recipe_form = RecipeForm()
    return render(request, "pages/recipe-create.html", {"recipe_form": recipe_form})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, owner=request.user)
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, instance=recipe)
        ingredient_names = request.POST.getlist("ingredient_name")
        ingredient_quantities = request.POST.getlist("ingredient_quantity")
        ingredient_serving = request.POST.getlist("ingredient_serving")
        ingredient_codes = request.POST.getlist("ingredient_code")
        ingredient_images = request.POST.getlist("ingredient_image")
        if recipe_form.is_valid():
            recipe_form.save()
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            for name, qty, srv, code, img in zip(ingredient_names, ingredient_quantities, ingredient_serving, ingredient_codes, ingredient_images):
                if name.strip():
                    ing = RecipeIngredient.objects.create(
                        recipe=recipe,
                        name=name.strip(),
                        quantity=qty.strip(),
                        serving_qty=int(srv) if srv else 100,
                        api_code=code.strip(),
                        api_image=img.strip(),
                    )
                    if code.strip():
                        _fetch_and_save_nutrition(ing, code.strip())
            messages.success(request, "Recepta actualitzada correctament.")
            return redirect("pages:recipe_detail", recipe_id=recipe.id)
        else:
            messages.error(request, "Si us plau, corregeix els errors del formulari.")
    recipe_form = RecipeForm(instance=recipe)
    return render(request, "pages/recipe-edit.html", {"recipe_form": recipe_form, "recipe": recipe})

@login_required
def search_ingredients_api(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"results": []})
    url = f"https://es.openfoodfacts.org/cgi/search.pl?search_terms={quote(query)}&action=process&json=1&page_size=10"
    headers = {"User-Agent": "flavorloop - Django - Version 1.0"}
    results = []
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        for p in data.get("products", []):
            name = p.get("product_name", "")
            if not name:
                continue
            code = p.get("code", "")
            image_url = p.get("image_url") or p.get("image_front_url") or ""
            nutriments = p.get("nutriments", {})
            results.append({
                "code": code,
                "name": name,
                "brands": p.get("brands", ""),
                "image": image_url,
                "nutriments": {
                    "kcal": nutriments.get("energy-kcal_100g", 0),
                    "fat": nutriments.get("fat_100g", 0),
                    "carbs": nutriments.get("carbohydrates_100g", 0),
                    "protein": nutriments.get("proteins_100g", 0),
                    "fiber": nutriments.get("fiber_100g", 0),
                    "salt": nutriments.get("salt_100g", 0),
                    "sugars": nutriments.get("sugars_100g", 0),
                }
            })
    except requests.RequestException:
        pass
    return JsonResponse({"results": results})

def _fetch_and_save_nutrition(ingredient, code):
    url = f"https://es.openfoodfacts.org/api/v2/product/{code}.json"
    headers = {"User-Agent": "flavorloop - Django - Version 1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        product = data.get("product", {})
        nutriments = product.get("nutriments", {})
        ingredient.nutrition_kcal = nutriments.get("energy-kcal_100g", 0)
        ingredient.nutrition_fat = nutriments.get("fat_100g", 0)
        ingredient.nutrition_carbs = nutriments.get("carbohydrates_100g", 0)
        ingredient.nutrition_protein = nutriments.get("proteins_100g", 0)
        ingredient.nutrition_fiber = nutriments.get("fiber_100g", 0)
        ingredient.nutrition_salt = nutriments.get("salt_100g", 0)
        ingredient.nutrition_sugars = nutriments.get("sugars_100g", 0)
        ingredient.save()
    except requests.RequestException:
        pass

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, owner=request.user)
    if request.method == "POST":
        recipe.delete()
        messages.success(request, "Recepta eliminada correctament.")
    return redirect("pages:recipes")

def search(request):
    query = request.GET.get("q", "").strip()
    products = []
    if query:
        url = f"https://es.openfoodfacts.org/cgi/search.pl?search_terms={quote(query)}&action=process&json=1&page_size=20"
        headers = {"User-Agent": "flavorloop - Django - Version 1.0"}
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            raw_products = data.get("products", [])
            for p in raw_products:
                name = p.get("product_name", "")
                if not name:
                    continue
                image_url = p.get("image_url") or p.get("image_front_url") or p.get("image_url_small", "")
                if image_url and not image_url.startswith("http"):
                    image_url = "https://es.openfoodfacts.org" + image_url
                nutriscore = p.get("nutriscore_grade", "unknown")
                if nutriscore and nutriscore != "unknown":
                    nutriscore = nutriscore.upper()
                brands = p.get("brands", "Marca desconeguda")
                quantity = p.get("quantity", "")
                products.append({
                    "name": name,
                    "brands": brands,
                    "nutriscore": nutriscore,
                    "image_url": image_url,
                    "quantity": quantity,
                })
        except requests.RequestException:
            messages.error(request, "No s'ha pogut connectar amb l'API d'Open Food Facts.")

    return render(request, "pages/search-results.html", {
        "query": query,
        "products": products,
    })


def social_placeholder(request):
    messages.info(request, "Aquesta funcionalitat estarà disponible properament.")
    return redirect("pages:login")
