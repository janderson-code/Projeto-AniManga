from email.policy import default
from django import forms
from season.models import Season
from .models import Manga, STATUS, SUBTYPES


class NewMangaForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = (
            'title',
            'kitsu_link',
            'subtype',
            'description',
            'total_chapters',
            'release_date',
            'status',
            'official_thumbnail',
            'custom_thumbnail',
            'serialization')

    title = forms.CharField(
        label="Título",
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
	
    kitsu_link = forms.CharField(
        label="Kitsu",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
				'placeholder': 'Coloque aqui o link do anime no Kitsu ou digite seu id',
                'class': 'form-control'
            }
        )
    )	
    release_date = forms.DateField(
        label="Data de lançamento",
        required=False,
        widget=forms.DateInput(attrs={
			'class': 'form-control',
			'type': 'date'
		})
    )

    description = forms.CharField(
        label="Descrição",
        max_length=255,
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subtype = forms.ChoiceField(
		choices = SUBTYPES, 
		label="Subtipo", 
		initial='', 
		widget=forms.Select(attrs={"class": 'form-controll browser-default'}), required=True)

    total_chapters = forms.IntegerField(
        label="Total de capitulos",
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
				'value': 0
			}
        )
    )
	
    status = forms.ChoiceField(
		choices = STATUS, 
		label="Status", 
		initial='', 
		widget=forms.Select(attrs={"class": 'form-controll browser-default'}), required=True)

    official_thumbnail = forms.CharField(
        label="Thumbnail oficial",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://media.kitsu.io/.../poster.jpg'
            }
        )
    )

    custom_thumbnail = forms.CharField(
        label="Thumbnail personalizado",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://meusmangas/.../manga-imagem.jpg'
            }
        )
    )

    serialization = forms.CharField(
        label="Serialização",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Shounen Drop'
            }
        )
    )


