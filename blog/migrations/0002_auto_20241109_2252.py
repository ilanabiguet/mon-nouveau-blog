# Generated by Django 2.2.28 on 2024-11-09 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipement',
            name='photo',
            field=models.URLField(),
        ),
    ]