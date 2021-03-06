# Generated by Django 4.0.4 on 2022-05-30 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('-date_joined',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddField(
            model_name='ordering',
            name='city',
            field=models.CharField(default='Чернігів', max_length=64, verbose_name='Город получателя'),
        ),
        migrations.AlterField(
            model_name='ordering',
            name='post_office',
            field=models.CharField(max_length=150, verbose_name='Почтовое отделение'),
        ),
        migrations.DeleteModel(
            name='PostOfices',
        ),
    ]
