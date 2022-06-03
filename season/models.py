from datetime import datetime
from django.db import models
from pkg_resources import require

# Create your models here.
SEASON_NAMES = (('Outono', 'Outono'), ('Inverno', 'Inverno'), ('Primavera', 'Primavera'), ('Verão', 'Verão'))

class Season(models.Model):
    season_name = models.CharField(max_length=255,choices=SEASON_NAMES, default='1',null=False)
    season_year = models.PositiveIntegerField(default=datetime.now().year, null=False)
    start_at = models.DateField()
    end_at = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Mostrando o titulo da temporada no Django Adm

    def __str__(self):
        return f"{self.season_name} - {self.season_year}"
