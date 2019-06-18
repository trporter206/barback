from django.urls import path
from . import views
from .models import Cocktail
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)

app_name = 'barapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('cocktail_form/', views.CreateView.as_view(model=Cocktail,
                                                    success_url=('http://127.0.0.1:8000/barapp/')),
                                                    name='cocktail_form'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('login/', LoginView.as_view(template_name='registration/login.html',
                                     redirect_field_name=('http://127.0.0.1:8000/barback/')),
                                     name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('<int:cocktail_id>/save/', views.save, name='save'),
    path('<int:cocktail_id>/delete/', views.delete, name='delete'),
]
