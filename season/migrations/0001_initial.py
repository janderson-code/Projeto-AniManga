# Generated by Django 4.0.4 on 2022-06-10 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_name', models.CharField(choices=[('Outono', 'Outono'), ('Inverno', 'Inverno'), ('Primavera', 'Primavera'), ('Verão', 'Verão')], default='1', max_length=255)),
                ('season_year', models.PositiveIntegerField(default=2022)),
                ('start_at', models.DateField()),
                ('end_at', models.DateField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
