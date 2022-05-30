from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AuthenticationFormCustom(AuthenticationForm):
	username = forms.CharField(label="Usuário")
	password = forms.CharField(label="Senha",widget=forms.PasswordInput)

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True,label='E-mail')
	username = forms.CharField(label="Usuário")
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