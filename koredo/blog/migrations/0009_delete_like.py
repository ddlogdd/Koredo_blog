# Generated by Django 5.0.4 on 2024-05-12 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_like'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]
