from django.db import models
from django.contrib.auth import get_user_model
from season.models import Season

# Create your models here.
STATUS = (
    ('Em andamento', 'Em andamento'), 
    ('Finalizado', 'Finalizado'),
    ('Não lançado','Não lançado'),
    ('Cancelado','Cancelado'),
    ('Pausado', 'Pausado'), 
    ('Desconhecido', 'Desconhecido')
)
SUBTYPES = (('TV', 'TV'), ('OVA', 'OVA'), ('ONA', 'ONA'),('Filme', 'Filme'), ('Outro', 'Outro'))


class Anime(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtype = models.CharField(max_length=255, choices=SUBTYPES)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    total_episodes = models.IntegerField()
    status = models.CharField(max_length=255, choices=STATUS)
    official_thumbnail = models.CharField(max_length=255)
    custom_thumbnail = models.CharField(max_length=255)
    studio = models.CharField(max_length=255)
    kitsu_link = models.CharField(max_length=255)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    # Mostrando o titulo do Anime no Django Adm

    def __str__(self):
        return f'Anime: {self.title} | Seasson: {self.season}'
