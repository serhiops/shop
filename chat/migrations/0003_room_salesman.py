# Generated by Django 4.0.4 on 2022-05-10 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='salesman',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='get_salesman_room', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]