from django.db import models

# Create your models here.
STATUS = (('Em andamento', 'Em andamento'), ('Finalizado', 'Finalizado'),
          ('Pausado', 'Pausado'), ('Cancelado', 'Cancelado'))


class Animes(models.Model):
    user_id = models.ForeignKey
    season_id = models.ForeignKey
    title = models.CharField(max_length=255)
    subtype = models.CharField(max_length=255)
    description = models.TextField()
    total_episodes = models.IntegerField()
    status = models.CharField(max_length=255, choices=STATUS)
    official_thumbnail = models.CharField(max_length=255)
    custom_thumbnail = models.CharField(max_length=255)
    studio = models.CharField(max_length=255)
    kitsu_link = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Mostrando o titulo do Anime no Django Adm

    def __str__(self):
        return self.title
