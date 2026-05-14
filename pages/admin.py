from django.contrib import admin
from .models import Recipe, RecipeIngredient, SavedRecipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "difficulty", "category", "prep_time_minutes", "created_at")
    list_filter = ("difficulty", "category", "created_at")
    search_fields = ("title", "description", "owner__username")

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "recipe", "quantity", "nutrition_kcal")
    list_filter = ("recipe",)
    search_fields = ("name", "recipe__title")

@admin.register(SavedRecipe)
class SavedRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe", "created_at")
    list_filter = ("created_at",)
