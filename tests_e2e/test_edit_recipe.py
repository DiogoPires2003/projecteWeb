"""
E2E tests for recipe editing (Deliverable 2 - Section 2, 3 points).

Tests cover:
- Owners can edit their own recipes
- Validation errors are shown when required fields are emptied
- Anonymous users are redirected to login
"""
import pytest
from pages.models import Recipe
from .conftest import PASSWORD, login_via_form


@pytest.mark.django_db
def test_owner_can_edit_recipe(page, live_server, user_a, recipe_of_a):
    """The owner of a recipe can edit it and see the changes."""
    login_via_form(page, live_server, "alice", PASSWORD)

    # Go to edit page for Alice's recipe
    page.goto(f"{live_server.url}/recipe/{recipe_of_a.id}/edit/")

    # Change the title and description
    page.fill('input[name="title"]', "Alice's UPDATED Pasta")
    page.fill('textarea[name="description"]', "Now with extra cheese")

    # Submit
    page.get_by_role("button", name="Update Recipe").click()

    # After saving, we are redirected to the detail page
    page.wait_for_url(f"{live_server.url}/recipe/{recipe_of_a.id}/", timeout=10000)

    # The DB record should be updated
    recipe_of_a.refresh_from_db()
    assert recipe_of_a.title == "Alice's UPDATED Pasta"
    assert recipe_of_a.description == "Now with extra cheese"


@pytest.mark.django_db
def test_edit_with_empty_title_shows_error(page, live_server, user_a, recipe_of_a):
    """Submitting the edit form with an empty title should not modify the recipe."""
    login_via_form(page, live_server, "alice", PASSWORD)

    original_title = recipe_of_a.title

    page.goto(f"{live_server.url}/recipe/{recipe_of_a.id}/edit/")

    # Empty the title
    page.fill('input[name="title"]', "")
    page.get_by_role("button", name="Update Recipe").click()

    # We should still be on the edit page (form re-rendered with errors)
    assert "/edit/" in page.url

    # The recipe in the DB must still have its original title
    recipe_of_a.refresh_from_db()
    assert recipe_of_a.title == original_title


@pytest.mark.django_db
def test_anonymous_cannot_edit_recipe(page, live_server, recipe_of_a):
    """Anonymous users trying to access the edit page are redirected to login."""
    page.goto(f"{live_server.url}/recipe/{recipe_of_a.id}/edit/")

    assert "/login/" in page.url