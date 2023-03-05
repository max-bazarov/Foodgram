# Generated by Django 4.1.5 on 2023-03-05 20:00

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0003_alter_recipe_cooking_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(
                choices=[("#42AAFF", "Blue"), ("#FF7777", "Red"), ("#78AD78", "Green")],
                default="#42AAFF",
                max_length=200,
                validators=[core.validators.validate_hex_color],
            ),
        ),
    ]