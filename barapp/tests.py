from django.test import RequestFactory, TestCase
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Cocktail, User
from datetime import datetime, timedelta
from .forms import CocktailForm
from .views import ProfileView

class CocktailFormTestCase(TestCase):
    def setUp(self):
        pub_time = timezone.now()
        cocktail = Cocktail.objects.create(cocktail_name   = "cocktail",
                                           pub_date        = pub_time,
                                           cocktail_info   = "info",
                                           cocktail_steps  = "steps",
                                           virgin          = False,)

    def test_init(self):
        cocktail = Cocktail.objects.get(cocktail_name="cocktail")
        CocktailForm({})

    def test_valid_data(self):
        form = CocktailForm({
            "cocktail_name" : "cocktail_name",
            "cocktail_type" : "WHISKEY",
            "cocktail_info" : "cocktail_info",
            "cocktail_steps": "cocktail_steps",
            "virgin"        : False,
        })
        self.assertTrue(form.is_valid())
        cocktail = form.save()
        self.assertEqual(cocktail.cocktail_name, "cocktail_name")
        self.assertEqual(cocktail.cocktail_type, "WHISKEY")
        self.assertEqual(cocktail.cocktail_info, "cocktail_info")
        self.assertEqual(cocktail.cocktail_steps, "cocktail_steps")
        self.assertEqual(cocktail.virgin, False)

    def test_blank_data(self):
        form = CocktailForm({})
        self.assertFalse(form.is_valid())

class CocktailTestCase(TestCase):
    def setUp(self):
        pub_time = timezone.now()
        Cocktail.objects.create(cocktail_name   ="cocktail",
                                pub_date        = pub_time,
                                cocktail_info   ="info",
                                cocktail_steps  ="steps",
                                cocktail_type   ="Whiskey",
                                virgin          = False,)
        Cocktail.objects.create(cocktail_name   ="virgin_cocktail",
                                pub_date        = pub_time,
                                cocktail_info   ="info",
                                cocktail_steps  ="steps",
                                cocktail_type   ="Vodka",
                                virgin          = True,)

    def test_cocktails_created(self):
        self.assertEqual(len(Cocktail.objects.all()), 2)

    def test_cocktail_is_virgin(self):
        virgin = Cocktail.objects.get(cocktail_name="virgin_cocktail")
        self.assertEqual(virgin.virgin, True)

    def test_cocktail_is_not_virgin(self):
        non_virgin = Cocktail.objects.get(cocktail_name="cocktail")
        self.assertEqual(non_virgin.virgin, False)

    def test_was_published_recently(self):
        cocktail = Cocktail.objects.get(cocktail_name = "cocktail")
        self.assertTrue(cocktail.was_published_recently())

    def test_string_fields_are_strings(self):
        cocktail = Cocktail.objects.get(cocktail_name="cocktail")
        self.assertTrue(isinstance(cocktail.cocktail_name, str))
        self.assertTrue(isinstance(cocktail.cocktail_info, str))
        self.assertTrue(isinstance(cocktail.cocktail_steps, str))

    def test_manhattan(self):
        manhattan = Cocktail.manhattan()
        self.assertEqual(manhattan.cocktail_name, "manhattan")

    def test_martini(self):
        martini = Cocktail.martini()
        self.assertEqual(martini.cocktail_name, "martini")

    def test_get_by_types(self):
        whiskey_list = [Cocktail.get_by_type("Whiskey")]
        vodka_list = [Cocktail.get_by_type("Vodka")]
        self.assertEqual(len(whiskey_list), 1)
        self.assertEqual(len(vodka_list), 1)
        Cocktail.manhattan()
        whiskey_list = Cocktail.get_by_type("Whiskey")
        self.assertEqual(len(whiskey_list), 2)
