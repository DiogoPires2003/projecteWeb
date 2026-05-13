from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    image_url = models.URLField(blank=True, default="")
    prep_time_minutes = models.PositiveIntegerField(default=0, help_text="Preparation time in minutes")
    servings = models.PositiveIntegerField(default=1)
    difficulty = models.CharField(
        max_length=20,
        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
        default="Easy",
    )
    category = models.CharField(max_length=100, blank=True, default="")
    instructions = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_total_nutrition(self):
        total = {"kcal": 0, "fat": 0, "carbs": 0, "protein": 0, "fiber": 0, "salt": 0, "sugars": 0}
        for ing in self.ingredients.all():
            total["kcal"] += ing.nutrition_kcal or 0
            total["fat"] += ing.nutrition_fat or 0
            total["carbs"] += ing.nutrition_carbs or 0
            total["protein"] += ing.nutrition_protein or 0
            total["fiber"] += ing.nutrition_fiber or 0
            total["salt"] += ing.nutrition_salt or 0
            total["sugars"] += ing.nutrition_sugars or 0
        return total

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_recipes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="saved_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "recipe")

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100, blank=True, default="")
    serving_qty = models.PositiveIntegerField(default=100, help_text="Grams per serving")

    nutrition_kcal = models.FloatField(default=0, blank=True, null=True)
    nutrition_fat = models.FloatField(default=0, blank=True, null=True)
    nutrition_carbs = models.FloatField(default=0, blank=True, null=True)
    nutrition_protein = models.FloatField(default=0, blank=True, null=True)
    nutrition_fiber = models.FloatField(default=0, blank=True, null=True)
    nutrition_salt = models.FloatField(default=0, blank=True, null=True)
    nutrition_sugars = models.FloatField(default=0, blank=True, null=True)

    api_code = models.CharField(max_length=50, blank=True, default="", help_text="Open Food Facts code")
    api_image = models.URLField(blank=True, default="")

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    def compute_scaled_nutrition(self):
        scale = self.serving_qty / 100.0
        return {
            "kcal": (self.nutrition_kcal or 0) * scale,
            "fat": (self.nutrition_fat or 0) * scale,
            "carbs": (self.nutrition_carbs or 0) * scale,
            "protein": (self.nutrition_protein or 0) * scale,
            "fiber": (self.nutrition_fiber or 0) * scale,
            "salt": (self.nutrition_salt or 0) * scale,
            "sugars": (self.nutrition_sugars or 0) * scale,
        }
