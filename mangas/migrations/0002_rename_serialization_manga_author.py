# Generated by Django 4.0.4 on 2022-06-03 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mangas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manga',
            old_name='serialization',
            new_name='author',
        ),
    ]
