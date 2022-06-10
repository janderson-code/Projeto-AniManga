from email.policy import default
from django import forms
from season.models import Season
from .models import Manga, STATUS, SUBTYPES


class NewMangaForm(forms.ModelForm):
	class Meta:
		model = Manga
		fields = (
			'kitsu_link',
			'auto_complete',
			'title',
			'subtype',
			'description',
			'total_chapters',
			'release_date',
			'status',
			'official_thumbnail',
			'custom_thumbnail',
			'author')
	auto_complete = forms.CharField(
		label="Preenche automaticamente o restante dos campos com kitsu",
		max_length=255,
		required=False,
		widget=forms.TextInput(
			attrs={
				'class': 'waves-effect waves-light btn-small disabled',
				'type':'button',
				'value': 'Pesquisar',
				'onclick': 'autoComplete()'
			}
		)
	) 
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
                'placeholder': 'Adicione o id, link ou nome do anime que deseja pesquisar',
				'class': 'form-control'
			}
		)
	)	
	release_date = forms.DateField(
		label="Data de lançamento",
		required=False,
		input_formats=['%Y-%m-%d'],
		widget=forms.DateInput(attrs={
			'class': 'form-control',
			'type': 'date'
		})
	)

	description = forms.CharField(
		label="Descrição",
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
		required=True,
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

	author = forms.CharField(
		label="Autor",
		max_length=255,
		required=False,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Kitsu Tanaka'
			}
		)
	)


