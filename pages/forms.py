from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required for password recovery')

    class Meta:
        model = User
        fields = ['username', 'email']

class RecipeForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=[("", "Select category"), ("Quick Meals", "Quick Meals"), ("Vegan", "Vegan"), ("High Protein", "High Protein"), ("Desserts", "Desserts"), ("Fitness", "Fitness")],
        required=False,
    )
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image_url', 'prep_time_minutes', 'servings', 'difficulty', 'category', 'instructions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 6}),
        }

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingredient name'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'e.g. 250g, 2 cups'}),
        }

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
