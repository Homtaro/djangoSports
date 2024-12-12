# Generated by Django 5.1.4 on 2024-12-11 20:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoSportApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='sportstructure',
            old_name='coordinates',
            new_name='address',
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.CheckConstraint(condition=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='rating_range'),
        ),
    ]
