from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Season


@admin.register(Season)
# Còdigo para apresentar botão de importação e exportação no admin page
class Season(ImportExportModelAdmin):
    pass
