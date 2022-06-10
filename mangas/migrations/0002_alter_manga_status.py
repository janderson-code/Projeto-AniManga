# Generated by Django 4.0.4 on 2022-06-10 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='status',
            field=models.CharField(choices=[('Em andamento', 'Em andamento'), ('Finalizado', 'Finalizado'), ('Não lançado', 'Não lançado'), ('Cancelado', 'Cancelado'), ('Pausado', 'Pausado'), ('Desconhecido', 'Desconhecido')], max_length=255),
        ),
    ]
