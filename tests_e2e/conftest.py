"""
Fixtures comuns per als tests E2E.

Aquests fixtures es comparteixen entre tots els tests del directori tests_e2e/.
"""
import pytest
from django.contrib.auth.models import User
from pages.models import Recipe

import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"

# Credencials estàndard per als usuaris de prova
PASSWORD = "TestPass123!"


@pytest.fixture
def user_a(db):
    """Crea i retorna l'usuari A ('alice')."""
    return User.objects.create_user(
        username="us_1",
        email="us_1@test.com",
        password=PASSWORD,
    )


@pytest.fixture
def user_b(db):
    """Crea i retorna l'usuari B ('bob')."""
    return User.objects.create_user(
        username="us_2",
        email="us_2@test.com",
        password=PASSWORD,
    )


@pytest.fixture
def recipe_of_a(user_a):
    """Crea una recepta propietat de l'usuari A."""
    return Recipe.objects.create(
        owner=user_a,
        title="Alice's Pasta",
        description="A simple pasta recipe",
        prep_time_minutes=20,
        servings=2,
        difficulty="Easy",
        category="Quick Meals",
        instructions="Boil water, cook pasta, serve.",
    )


def login_via_form(page, live_server, username, password):
    """
    Helper per fer login mitjançant el formulari real (E2E),
    no mitjançant atalls de Django.
    """
    page.goto(f"{live_server.url}/login/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.locator("#submit-btn").click()
    # Espera a ser redirigit a la home després del login
    page.wait_for_url(f"{live_server.url}/")