from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
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


def social_placeholder(request):
    messages.info(request, "Aquesta funcionalitat estarà disponible properament.")
    return redirect("pages:login")

