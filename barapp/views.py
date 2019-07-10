import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic, View
from .models import Cocktail, User
from django.urls import reverse
from django.db import models
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from .forms import (
    CocktailForm,
    UserForm,
    EditProfileForm,
)
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm
)
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash
)
from django.contrib.auth.models import User

class IndexView(generic.ListView):
    template_name = 'barapp/index.html'
    context_object_name = 'latest_cocktails'

    def get_queryset(self):
        return Cocktail.objects.order_by('-pub_date')

def detail(request, cocktail_id):
    cocktail = Cocktail.objects.get(id=cocktail_id)
    user = request.user
    is_favorite = False
    if cocktail.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    context = {
        'cocktail'    : cocktail,
        'is_favorite' : is_favorite,
    }

    return render(request, 'barapp/detail.html', context)

def favorite(request, cocktail_id):
    cocktail = get_object_or_404(Cocktail, id=cocktail_id)
    if cocktail.favorite.filter(id=request.user.id).exists():
        cocktail.favorite.remove(request.user)
    else:
        cocktail.favorite.add(request.user)
    return HttpResponseRedirect(cocktail.get_absolute_url())

def favorites_list(request):
    user = request.user
    favorite_cocktails = user.favorite.all()


class CreateView(generic.edit.CreateView):
    model = Cocktail
    fields = ['cocktail_name',
              'cocktail_type',
              'cocktail_image',
              'cocktail_info',
              'cocktail_steps',
              'virgin',
              ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def save(request, cocktail_id):
    form = CocktailForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(reverse('barapp:detail', args=(cocktail.id,)))

def delete(request, cocktail_id):
    model = get_object_or_404(Cocktail, pk=cocktail_id)
    model.delete()
    return HttpResponseRedirect(reverse('barapp:index'))

class AboutView(generic.TemplateView):
    template_name = 'barapp/about.html'

def profile(request):
    user = request.user
    user_cocktails = Cocktail.objects.filter(user=user).order_by('-pub_date')
    fav_cocktails  = Cocktail.objects.filter(favorite=user.id)

    context = {
        'user_cocktails' : user_cocktails,
        'fav_cocktails'  : fav_cocktails,
    }

    return render(request, 'barapp/profile.html', context)

class RegisterView(generic.edit.CreateView):
    template_name = 'registration/registration_form.html'
    form_class    = UserForm

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username_iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = "Username is already taken"
    return JsonResponse(data)

def logout_view(request):
    logout(request)
    return redirect('barapp:index')
