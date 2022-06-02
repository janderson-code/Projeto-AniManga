from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Manga


@admin.register(Manga)
#Còdigo para apresentar botão de importação e exportação no admin page
class Manga(ImportExportModelAdmin):
    pass
