from django.db import models

# Create your models here.


class season(models.Model):
    season_name = models.CharField(max_length=255)
    season_year = models.DateTimeField()
    total_animes = models.IntegerField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Mostrando o titulo da temporada no Django Adm

    def __str__(self):
        return self.title
