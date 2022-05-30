from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AuthenticationFormCustom(AuthenticationForm):
	username = forms.CharField(label="Usuário",error_messages={'required': 'Esse campo não deve estar vazio.'})
	password = forms.CharField(label="Senha",error_messages={'required': 'Esse campo não deve estar vazio.'},widget=forms.PasswordInput)
	error_messages = {
			'invalid_login': ("Por favor, insira um nome de usuário e senha válidos. Note que ambos os campos diferenciam maiúsculas e minúsculas."),
	}
	class Meta:
		model = User
		fields = ('username', 'password')


class NewUserForm(UserCreationForm):

	error_messages={
		'password_mismatch': ("As senhas não são iguais."),
	}
	email = forms.EmailField(required=True,label='E-mail',error_messages={
			'required': 'Esse campo não deve estar vazio.',
			'invalid': 'Insira um e-mail válido.',
			'unique': 'Esse e-mail já está em uso.'
	})
	username = forms.CharField(label="Usuário",error_messages={
		'unique': ("Esse nome de usuário já existe. Por favor, escolha outro."),
		'required': ("Esse campo não deve estar vazio."),
		'invalid': ("Por favor, insira um nome de usuário válido."),
	})
	password1 = forms.CharField(label="Senha",widget=forms.PasswordInput)
	password2 = forms.CharField(label="Senha Confirmação",widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user