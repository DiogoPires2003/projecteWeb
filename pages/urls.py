from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("social-login/", views.social_placeholder, name="social_login"),
    path("settings/", views.settings, name="settings"),
    path("ingredient/", views.ingredient_info, name="ingredient_info"),
    path("recipe/", views.recipe_info, name="recipe_info"),
    path("ingredients/", views.ingredients, name="ingredients"),
    path("recipes/", views.recipes, name="recipes"),
    
    # Password Reset (Django built-in)
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='pages/password_reset.html',
             success_url=reverse_lazy('pages:password_reset_done')
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='pages/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='pages/password_reset_confirm.html',
             success_url=reverse_lazy('pages:password_reset_complete')
         ), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='pages/password_reset_complete.html'), 
         name='password_reset_complete'),
]

