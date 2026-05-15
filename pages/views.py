from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import requests
from urllib.parse import quote
from .models import Recipe, RecipeIngredient, SavedRecipe, CachedIngredient
from .forms import (
    UserRegisterForm, RecipeForm, RecipeIngredientForm, ProfileForm
)

def search_recipes_api(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    if not query and not category:
        recipes = Recipe.objects.all().select_related("owner").order_by("-created_at")[:20]
    elif category == "Quick Meals":
        recipes = Recipe.objects.filter(prep_time_minutes__lt=16).select_related("owner").order_by("-created_at")[:20]
    elif category:
        recipes = Recipe.objects.filter(category__icontains=category).select_related("owner").order_by("-created_at")[:20]
    else:
        recipes = Recipe.objects.filter(title__icontains=query).select_related("owner").order_by("-created_at")[:20]
    saved_ids = set()
    if request.user.is_authenticated:
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
    default_recipes = Recipe.objects.all().select_related("owner").order_by("-created_at")[:14]
    saved_ids = set()
    if request.user.is_authenticated:
        saved_ids = set(SavedRecipe.objects.filter(user=request.user).values_list("recipe_id", flat=True))
    recipes_data = []
    for r in default_recipes:
        recipes_data.append({
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
    return render(request, "pages/home.html", {
        "default_recipes": recipes_data,
        "mood_categories": [
            {"slug": "Quick Meals", "label": "Quick Meals", "icon": "timer"},
            {"slug": "Vegan", "label": "Vegan", "icon": "eco"},
            {"slug": "High Protein", "label": "High Protein", "icon": "fitness_center"},
            {"slug": "Desserts", "label": "Desserts", "icon": "bakery_dining"},
            {"slug": "Discover", "label": "Discover", "icon": "more_horiz"},
        ]
    })

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
    else:
        recipe_form = RecipeForm()
        ingredient_names = ingredient_quantities = ingredient_serving = ingredient_codes = ingredient_images = []
    ingredients_data = []
    for name, qty, srv, code, img in zip(ingredient_names, ingredient_quantities, ingredient_serving, ingredient_codes, ingredient_images):
        if name.strip():
            ingredients_data.append({
                "name": name.strip(), "quantity": qty.strip(),
                "serving": srv, "code": code.strip(), "image": img.strip(),
            })
    return render(request, "pages/recipe-create.html", {
        "recipe_form": recipe_form,
        "ingredients_data": ingredients_data,
    })

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
    else:
        recipe_form = RecipeForm(instance=recipe)
        ingredient_names = ingredient_quantities = ingredient_serving = ingredient_codes = ingredient_images = []
    ingredients_data = []
    for name, qty, srv, code, img in zip(ingredient_names, ingredient_quantities, ingredient_serving, ingredient_codes, ingredient_images):
        if name.strip():
            ingredients_data.append({
                "name": name.strip(), "quantity": qty.strip(),
                "serving": srv, "code": code.strip(), "image": img.strip(),
            })
    return render(request, "pages/recipe-edit.html", {
        "recipe_form": recipe_form, "recipe": recipe,
        "ingredients_data": ingredients_data,
    })

def search_ingredients_api(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"results": []})
    
    seen_codes = set()
    results = []
    api_success = False
    
    url = f"https://es.openfoodfacts.org/cgi/search.pl?search_terms={quote(query)}&action=process&json=1&page_size=10"
    headers = {"User-Agent": "flavorloop - Django - Version 1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        api_success = True
        for p in data.get("products", []):
            name = p.get("product_name", "")
            if not name:
                continue
            code = p.get("code", "")
            if code:
                seen_codes.add(code)
            image_url = p.get("image_url") or p.get("image_front_url") or ""
            nutriments = p.get("nutriments", {})
            entry = {
                "code": code,
                "name": name,
                "brands": p.get("brands", ""),
                "image": image_url,
                "cached": False,
                "nutriments": {
                    "kcal": nutriments.get("energy-kcal_100g", 0),
                    "fat": nutriments.get("fat_100g", 0),
                    "carbs": nutriments.get("carbohydrates_100g", 0),
                    "protein": nutriments.get("proteins_100g", 0),
                    "fiber": nutriments.get("fiber_100g", 0),
                    "salt": nutriments.get("salt_100g", 0),
                    "sugars": nutriments.get("sugars_100g", 0),
                }
            }
            results.append(entry)
            if code:
                CachedIngredient.objects.update_or_create(
                    api_code=code,
                    defaults={
                        "name": name,
                        "brands": p.get("brands", ""),
                        "image": image_url,
                        "nutrition_kcal": nutriments.get("energy-kcal_100g", 0),
                        "nutrition_fat": nutriments.get("fat_100g", 0),
                        "nutrition_carbs": nutriments.get("carbohydrates_100g", 0),
                        "nutrition_protein": nutriments.get("proteins_100g", 0),
                        "nutrition_fiber": nutriments.get("fiber_100g", 0),
                        "nutrition_salt": nutriments.get("salt_100g", 0),
                        "nutrition_sugars": nutriments.get("sugars_100g", 0),
                    }
                )
    except requests.RequestException:
        pass

    if not api_success or len(results) < 10:
        cached = CachedIngredient.objects.filter(name__icontains=query).exclude(api_code__in=seen_codes)[:10]
        for c in cached:
            results.append(c.to_dict() | {"cached": True})
    
    return JsonResponse({"results": results})

def _fetch_and_save_nutrition(ingredient, code):
    cached = CachedIngredient.objects.filter(api_code=code).first()
    if cached and not cached.is_stale(hours=24):
        ingredient.nutrition_kcal = cached.nutrition_kcal
        ingredient.nutrition_fat = cached.nutrition_fat
        ingredient.nutrition_carbs = cached.nutrition_carbs
        ingredient.nutrition_protein = cached.nutrition_protein
        ingredient.nutrition_fiber = cached.nutrition_fiber
        ingredient.nutrition_salt = cached.nutrition_salt
        ingredient.nutrition_sugars = cached.nutrition_sugars
        ingredient.save()
        return

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
        CachedIngredient.objects.update_or_create(
            api_code=code,
            defaults={
                "name": product.get("product_name", ingredient.name),
                "brands": product.get("brands", ""),
                "image": product.get("image_url") or product.get("image_front_url") or "",
                "nutrition_kcal": nutriments.get("energy-kcal_100g", 0),
                "nutrition_fat": nutriments.get("fat_100g", 0),
                "nutrition_carbs": nutriments.get("carbohydrates_100g", 0),
                "nutrition_protein": nutriments.get("proteins_100g", 0),
                "nutrition_fiber": nutriments.get("fiber_100g", 0),
                "nutrition_salt": nutriments.get("salt_100g", 0),
                "nutrition_sugars": nutriments.get("sugars_100g", 0),
            }
        )
    except requests.RequestException:
        if cached:
            ingredient.nutrition_kcal = cached.nutrition_kcal
            ingredient.nutrition_fat = cached.nutrition_fat
            ingredient.nutrition_carbs = cached.nutrition_carbs
            ingredient.nutrition_protein = cached.nutrition_protein
            ingredient.nutrition_fiber = cached.nutrition_fiber
            ingredient.nutrition_salt = cached.nutrition_salt
            ingredient.nutrition_sugars = cached.nutrition_sugars
            ingredient.save()

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
    api_success = False
    if query:
        url = f"https://es.openfoodfacts.org/cgi/search.pl?search_terms={quote(query)}&action=process&json=1&page_size=20"
        headers = {"User-Agent": "flavorloop - Django - Version 1.0"}
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            api_success = True
            raw_products = data.get("products", [])
            for p in raw_products:
                name = p.get("product_name", "")
                if not name:
                    continue
                code = p.get("code", "")
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
                if code:
                    nutriments = p.get("nutriments", {})
                    CachedIngredient.objects.update_or_create(
                        api_code=code,
                        defaults={
                            "name": name,
                            "brands": brands,
                            "image": image_url,
                            "nutrition_kcal": nutriments.get("energy-kcal_100g", 0),
                            "nutrition_fat": nutriments.get("fat_100g", 0),
                            "nutrition_carbs": nutriments.get("carbohydrates_100g", 0),
                            "nutrition_protein": nutriments.get("proteins_100g", 0),
                            "nutrition_fiber": nutriments.get("fiber_100g", 0),
                            "nutrition_salt": nutriments.get("salt_100g", 0),
                            "nutrition_sugars": nutriments.get("sugars_100g", 0),
                        }
                    )
        except requests.RequestException:
            messages.error(request, "No s'ha pogut connectar amb l'API d'Open Food Facts.")

        if not api_success:
            cached = CachedIngredient.objects.filter(name__icontains=query)[:20]
            for c in cached:
                products.append({
                    "name": c.name,
                    "brands": c.brands,
                    "nutriscore": "unknown",
                    "image_url": c.image,
                    "quantity": "",
                })

    return render(request, "pages/search-results.html", {
        "query": query,
        "products": products,
    })


def social_placeholder(request):
    messages.info(request, "Aquesta funcionalitat estarà disponible properament.")
    return redirect("pages:login")
