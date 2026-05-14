"""
E2E tests for recipe deletion (Deliverable 2 - Section 3, 1.5 points).

Tests cover:
- Owners can delete their own recipes
- Anonymous users cannot delete recipes
"""
import pytest
from pages.models import Recipe
from .conftest import PASSWORD, login_via_form


@pytest.mark.django_db
def test_owner_can_delete_recipe(page, live_server, user_a, recipe_of_a):
    """The owner of a recipe can delete it and the recipe is removed from the DB."""
    login_via_form(page, live_server, "alice", PASSWORD)

    recipe_id = recipe_of_a.id

    # Go to user's recipe list (where the Delete button lives)
    page.goto(f"{live_server.url}/recipes/")

    # The template uses a JS confirm() dialog. Auto-accept it.
    page.on("dialog", lambda dialog: dialog.accept())

    # Click the Delete button
    page.get_by_role("button", name="Delete").click()

    # Wait until the page reloads to /recipes/ (after deletion)
    page.wait_for_url(f"{live_server.url}/recipes/", timeout=10000)

    # The recipe must no longer be in the DB
    assert not Recipe.objects.filter(id=recipe_id).exists()

    # And it must no longer be visible in the page
    assert not page.locator(f"text={recipe_of_a.title}").is_visible()


@pytest.mark.django_db
def test_anonymous_cannot_delete_recipe(page, live_server, recipe_of_a):
    """Anonymous users cannot reach the delete URL — they are redirected to login.

    Note: the delete view requires POST, but the @login_required decorator
    intercepts the request before that and redirects to /login/.
    """
    recipe_id = recipe_of_a.id

    # Anonymous GET to the delete URL: redirected to login
    page.goto(f"{live_server.url}/recipe/{recipe_id}/delete/")
    assert "/login/" in page.url

    # The recipe must still exist
    assert Recipe.objects.filter(id=recipe_id).exists()