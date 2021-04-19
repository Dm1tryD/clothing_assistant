from django.db import models
from django.urls import reverse

from django.utils.text import slugify


def gen_slug(s):
    new_slug = slugify(str(s).lower().replace(' ', '-'), allow_unicode=True)
    return new_slug


class ClothingCategory(models.Model):

    category_name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Clothing category"
        verbose_name_plural = "Clothing categories"

    def __str__(self):
        return self.category_name


class Season(models.Model):

    season_name = models.CharField(max_length=15)
    slug = models.SlugField(max_length=15, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Seasons'

    def __str__(self):
        return self.season_name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = gen_slug(self.season_name)
        super().save(*args, *kwargs)

    def get_absolute_url(self):
        return reverse('styles_page', kwargs={'season': self.slug})


class ClothingSubCategory(models.Model):
    """Stores all the names and id of the subcategory of the main categories"""

    GENDER_CHOISES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Universal')
    )
    clothing_category = models.ForeignKey(ClothingCategory, on_delete=models.CASCADE, related_name="clothing_category")
    subcategory = models.CharField(max_length=255)
    subcategory_store_num = models.IntegerField(unique=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="season")
    gender = models.CharField(max_length=1, choices=GENDER_CHOISES)

    class Meta:
        verbose_name = "Clothing subcategory"
        verbose_name_plural = "Clothing subcategories"

    def __str__(self):
        return f"Gender: {self.gender}, Season: {self.season.season_name}, {self.clothing_category.category_name}," \
               f"{self.subcategory}"


class StyleCategory(models.Model):
    """Stores user-created clothing styles"""

    style_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    item = models.ManyToManyField('ClothingSubCategory', related_name="item")
    colour = models.ManyToManyField('Colour', related_name="colour")
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Style category"
        verbose_name_plural = "Style categories"

    def __str__(self):
        return self.style_name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = gen_slug(self.style_name)
        super().save(*args, *kwargs)


class Colour(models.Model):
    """Colours id"""

    colour_name = models.CharField(max_length=255)
    colour_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.colour_name


class CountrySettings(models.Model):

    country = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    store = models.CharField(max_length=255)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = 'Country settings'
