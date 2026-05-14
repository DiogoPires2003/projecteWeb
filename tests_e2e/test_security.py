"""
E2E security tests (Deliverable 2 - transversal requirement).

The deliverable explicitly requires testing how 'relevant security
restrictions are addressed'. These tests cover ownership boundaries:
authenticated users must NOT be able to edit or delete recipes that
belong to a different user.
"""
import pytest
from pages.models import Recipe
from .conftest import PASSWORD, login_via_form


@pytest.mark.django_db
def test_user_cannot_edit_others_recipe(page, live_server, user_a, user_b, recipe_of_a):
    """Bob (logged in) tries to edit Alice's recipe and gets a 404."""
    # Log in as Bob, not as the owner
    login_via_form(page, live_server, "bob", PASSWORD)

    original_title = recipe_of_a.title

    # Try to access Alice's edit page
    response = page.goto(f"{live_server.url}/recipe/{recipe_of_a.id}/edit/")

    # The server should return 404 (Django's get_object_or_404)
    assert response.status == 404

    # Even if somehow he tried to submit, the title should remain unchanged
    recipe_of_a.refresh_from_db()
    assert recipe_of_a.title == original_title


@pytest.mark.django_db
def test_user_cannot_delete_others_recipe(page, live_server, user_a, user_b, recipe_of_a):
    """Bob (logged in) tries to delete Alice's recipe and gets a 404, recipe stays in DB."""
    login_via_form(page, live_server, "bob", PASSWORD)

    recipe_id = recipe_of_a.id

    # Direct GET to delete URL: the view will 404 because owner != bob
    response = page.goto(f"{live_server.url}/recipe/{recipe_id}/delete/")

    # 404, recipe still exists
    assert response.status == 404
    assert Recipe.objects.filter(id=recipe_id).exists()


@pytest.mark.django_db
def test_user_does_not_see_others_recipes_in_their_list(page, live_server, user_a, user_b, recipe_of_a):
    """Bob's /recipes/ page should only list Bob's recipes, not Alice's."""
    login_via_form(page, live_server, "bob", PASSWORD)

    page.goto(f"{live_server.url}/recipes/")

    # Alice's recipe should NOT appear on Bob's list
    assert not page.locator(f"text={recipe_of_a.title}").is_visible()