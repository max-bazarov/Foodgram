from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.validators import validate_hex_color


class Tag(models.Model):
    class Color(models.TextChoices):
        BLUE = '#42AAFF'
        RED = '#FF7777'
        GREEN = '#78AD78'

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    color = models.CharField(
        max_length=200,
        validators=[validate_hex_color],
        choices=Color.choices,
        default=Color.BLUE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    author = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='recipes'
    )
    name = models.CharField(
        max_length=200,
    )
    text = models.TextField()
    image = models.ImageField(upload_to='images/')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', related_name='recipes'
    )
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ['-id']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipe'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
    )
