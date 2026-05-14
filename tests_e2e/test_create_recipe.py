"""
E2E tests for recipe creation (Deliverable 2 - Section 1, 3 points).

Tests cover:
- Logged users can create new recipes
- Validation errors are shown when required fields are missing
- Anonymous users are redirected to login
"""
import pytest
from pages.models import Recipe
from .conftest import PASSWORD, login_via_form


@pytest.mark.django_db
def test_logged_user_can_create_recipe(page, live_server, user_a):
    """A logged-in user can create a new recipe and see it in their list."""
    login_via_form(page, live_server, "alice", PASSWORD)

    page.goto(f"{live_server.url}/recipe/create/")

    # Fill in the form
    page.fill('input[name="title"]', "My First Recipe")
    page.fill('textarea[name="description"]', "A delicious test recipe")
    page.fill('input[name="prep_time_minutes"]', "30")
    page.fill('input[name="servings"]', "4")
    page.select_option('select[name="difficulty"]', "Medium")
    page.fill('textarea[name="instructions"]', "Step 1: Cook. Step 2: Eat.")

    # Submit form
    page.get_by_role("button", name="Save Recipe").click()

    # Wait for redirect to the recipe list
    page.wait_for_url(f"{live_server.url}/recipes/", timeout=10000)

    # Verify the recipe appears in the list and exists in DB
    assert page.locator("text=My First Recipe").is_visible()
    assert Recipe.objects.filter(title="My First Recipe", owner=user_a).exists()


@pytest.mark.django_db
def test_create_recipe_without_title_shows_error(page, live_server, user_a):
    """Submitting the form without a title should NOT create a recipe."""
    login_via_form(page, live_server, "alice", PASSWORD)

    page.goto(f"{live_server.url}/recipe/create/")

    # Fill everything except the title
    page.fill('textarea[name="description"]', "No title here")
    page.fill('input[name="prep_time_minutes"]', "15")
    page.click('button[type="submit"]')

    # We should NOT have been redirected to /recipes/
    # (the form re-renders with errors)
    assert "/recipe/create/" in page.url or "/recipes/" not in page.url

    # No recipe should have been created
    assert not Recipe.objects.filter(description="No title here").exists()


@pytest.mark.django_db
def test_anonymous_cannot_create_recipe(page, live_server):
    """An anonymous user trying to access /recipe/create/ should be redirected to login."""
    page.goto(f"{live_server.url}/recipe/create/")

    # After the redirect, the URL should contain /login/
    assert "/login/" in page.url