from django.urls import path
from . import views, static
from .models import Cocktail
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)

app_name = 'barapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:cocktail_id>/', views.detail, name='detail'),
    path('cocktail_form/', views.CreateView.as_view(model=Cocktail,
                                                    success_url=('http://127.0.0.1:8000/barapp/')),
                                                    name='cocktail_form'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('login/', LoginView.as_view(template_name='registration/login.html',
                                     redirect_field_name=('http://127.0.0.1:8000/barback/')),
                                     name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('<int:cocktail_id>/save/', views.save, name='save'),
    path('<int:cocktail_id>/delete/', views.delete, name='delete'),
    path('<int:cocktail_id>/favorite/', views.favorite, name='favorite'),
    path('cabinet/', views.CabinetView.as_view(), name='cabinet'),
    path('ajax/add_to_cabinet/', views.add_to_cabinet, name='add_to_cabinet'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
