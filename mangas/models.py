from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

STATUS = (
    ('Em andamento', 'Em andamento'), 
    ('Finalizado', 'Finalizado'),
    ('Não lançado','Não lançado'),
    ('Cancelado','Cancelado'),
    ('Pausado', 'Pausado'), 
    ('Desconhecido', 'Desconhecido')
)
SUBTYPES = (('Manga', 'Manga'), ('One-shot', 'One-shot'))

class Manga(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtype = models.CharField(max_length=255)
    description = models.TextField()
    total_chapters = models.IntegerField()
    status = models.CharField(max_length=255, choices=STATUS)
    official_thumbnail = models.CharField(max_length=255)
    custom_thumbnail = models.CharField(max_length=255)
    kitsu_link = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    release_date = models.DateField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Mostrando o titulo do Mangá no Django Adm

    def __str__(self):
        return self.title
