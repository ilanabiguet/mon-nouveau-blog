# Generated by Django 2.2.28 on 2024-11-09 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20241109_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='photo',
            field=models.URLField(),
        ),
    ]