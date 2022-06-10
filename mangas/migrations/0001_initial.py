# Generated by Django 4.0.4 on 2022-06-10 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtype', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('total_chapters', models.IntegerField()),
                ('status', models.CharField(choices=[('Em andamento', 'Em andamento'), ('Finalizado', 'Finalizado'), ('Não lançado', 'Não lançado'), ('Cancelado', 'Cancelado'), ('Pausado', 'Pausado'), ('Desconhecido', 'Desconhecido')], max_length=255)),
                ('official_thumbnail', models.CharField(max_length=255)),
                ('custom_thumbnail', models.CharField(max_length=255)),
                ('kitsu_link', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('release_date', models.DateField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
