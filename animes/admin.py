from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Anime


@admin.register(Anime)
# Còdigo para apresentar botão de importação e exportação no admin page
class Anime(ImportExportModelAdmin):
    pass
