from django.db import models


class Recipe(models.Model):
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes',
        through='RecipeIngredient'
    )
    tag = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        through='RecipeTag'
    )
    cooking_time = models.IntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    color = models.CharField(max_length=200)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField()
    unit = models.CharField(max_length=200)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipe_tags'
    )
