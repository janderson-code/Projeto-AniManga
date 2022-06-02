from datetime import datetime,timedelta
from django import forms
from .models import Season, SEASON_NAMES


now = datetime.now()

class NewSeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = (
            'season_name',
            'season_year',
            'start_at',
            'end_at',
        )

    season_name = forms.ChoiceField(
        choices=SEASON_NAMES,
        required=True,
        label="Período do Ano",
        initial='1',
        widget=forms.Select(attrs={"class": 'form-controll browser-default'})
    )

    season_year = forms.IntegerField(
        label="Ano",
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'value': now.year,
                'onchange': 'changeDateYear(this.value)',
            }
        )
    )

    start_at = forms.DateField(
        label="Data de início",
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'value': now.strftime('%Y-%m-%d')
            }
        )
    )

    end_at = forms.DateField(
        label="Data de término",
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'value': (now + timedelta(days=90)).strftime('%Y-%m-%d')
            }
        )
    )
