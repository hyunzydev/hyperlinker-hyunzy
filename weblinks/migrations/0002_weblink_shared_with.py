# Generated by Django 4.2.11 on 2025-02-19 08:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("weblinks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="weblink",
            name="shared_with",
            field=models.ManyToManyField(
                blank=True, related_name="shared_weblinks", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
