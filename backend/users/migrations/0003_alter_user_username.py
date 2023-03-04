# Generated by Django 4.1.5 on 2023-02-24 09:37

from django.db import migrations, models

import core.validators


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_managers_alter_user_date_joined_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=255,
                unique=True,
                validators=[core.validators.validate_username],
                verbose_name="username",
            ),
        ),
    ]
