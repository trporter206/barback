from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
from django.conf import settings
from django.urls import reverse


class User(AbstractUser):
    bartender = models.BooleanField(null=True)

    def get_absolute_url(self):
        return reverse("barapp:profile", kwargs={"id": self.id})

class Cocktail(models.Model):
    slug            = models.SlugField(max_length=120, blank=True)
    cocktail_name   = models.CharField(max_length = 50)
    cocktail_image  = models.ImageField(upload_to="cocktail_images/",
                                        blank=True,
                                        null=True)
    pub_date        = models.DateTimeField(auto_now=True)
    cocktail_info   = models.CharField(max_length = 200, blank=True, null=True)
    virgin          = models.BooleanField(null=True)
    favorite        = models.ManyToManyField(User, related_name='favorite', blank=True)
    user            = models.ForeignKey(User, on_delete= models.CASCADE, blank=True,
                                                                         null=True)

    cocktail_type_choices = (
        ('WHISKEY', 'Whiskey'),
        ('VODKA', 'Vodka'),
        ('TEQUILA', 'Tequila'),
        ('GIN', 'Gin'),
        ('VIRGIN', 'Virgin'),
    )
    cocktail_type = models.CharField(max_length = 10, choices = cocktail_type_choices)

    def __str__(self):
        return self.cocktail_name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=2) <= self.pub_date <= now

    def get_absolute_url(self):
        return reverse("barapp:detail", kwargs={"cocktail_id": self.id})

    @classmethod
    def manhattan(cls):
        manhattan = cls.objects.create(cocktail_name  = "manhattan",
                                       cocktail_info  = "a classic drink",
                                       cocktail_type  = "Whiskey",
                                       virgin         =  False,)
        return manhattan

    @classmethod
    def martini(cls):
        martini = cls.objects.create(cocktail_name  = "martini",
                                       cocktail_info  = "youve seen bond",
                                       cocktail_type  = "Vodka",
                                       virgin         =  False,)
        return martini

    @classmethod
    def get_by_type(cls, type):
        cocktails = cls.objects.filter(cocktail_type = type)
        return cocktails

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class CocktailSteps(models.Model):
    step     = models.CharField(max_length = 100)
    cocktail = models.ForeignKey(Cocktail, on_delete= models.CASCADE, blank=True,
                                                                      null=True)

class CocktailIngredients(models.Model):
    ingredient = models.CharField(max_length = 50)
    quantity   = models.IntegerField(null = True)

    ingredient_units = (
        ('PART', 'part'),
        ('OZ', 'oz'),
        ('FL OZ', 'fl oz'),
        ('ML', 'ml'),
        ('PINCH', 'pinch'),
        ('WEDGE', 'wedge'),
        ('DROP', 'drop'),
        ('SPLASH', 'splash'),
        ('TBSP', 'tbsp'),
        ('TSP', 'tsp'),
    )

    unit       = models.CharField(max_length = 10, choices = ingredient_units)
    cocktail   = models.ForeignKey(Cocktail, on_delete= models.CASCADE, blank=True,
                                                                        null=True)
