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

class DetailView(generic.DetailView):
    model = Cocktail
    template_name = 'barapp/detail.html'

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

class ProfileView(generic.ListView):
    template_name = 'barapp/profile.html'
    context_object_name = 'user_cocktails'

    def get_queryset(self):
        return Cocktail.objects.filter(user = self.request.user).order_by('-pub_date')

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
