from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import requests
from urllib.parse import quote
from .forms import UserRegisterForm

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
    return render(request, "pages/settings.html")

def ingredient_info(request):
    return render(request, "pages/ingredient-info.html")

def recipe_info(request):
    return render(request, "pages/recipe-info.html")

def ingredients(request):
    return render(request, "pages/ingredients.html")

def recipes(request):
    return render(request, "pages/recipes.html")

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


def search(request):
    query = request.GET.get("q", "").strip()
    products = []
    if query:
        url = f"https://es.openfoodfacts.org/cgi/search.pl?search_terms={quote(query)}&action=process&json=1&page_size=20"
        headers = {
            "User-Agent": "flavorloop - Django - Version 1.0"
        }
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            raw_products = data.get("products", [])
            for p in raw_products:
                name = p.get("product_name", "")
                if not name:
                    continue
                image_url = p.get("image_url_small") or p.get("image_front_small_url") or p.get("image_front_url") or p.get("image_url", "")
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

