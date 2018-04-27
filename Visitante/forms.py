from django import forms
from django.utils import timezone
from django.contrib.auth.models import Group

from Usuarios.models import User


class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirme a Senha', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("email is taken")
		return email

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class StudentRegisterForm(RegisterForm):
	nascimento = forms.DateField(label='Nascimento', widget=forms.SelectDateWidget(years=[y for y in range(timezone.now().year, timezone.now().year - 100, -1)]))
	ingresso_ensino_medio = forms.DateField(label='Ingresso no Ensio Médio', widget=forms.SelectDateWidget(years=[y for y in range(timezone.now().year, timezone.now().year - 50, -1)]))
	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirme a Senha', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'primeiro_nome', 'segundo_nome', 'genero', 'cep')

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.nascimento = self.cleaned_data['nascimento']
		user.ingresso_ensino_medio = self.cleaned_data['ingresso_ensino_medio']
		user.genero = self.cleaned_data['genero']
		if commit:
			user.save()
			a = Group.objects.get(name='Alunos') 
			user.groups.add(a)
			user.save()
		return user

class TeacherRegisterForm(RegisterForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2
		
	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
			p = Group.objects.get(name='Corretores') 
			user.groups.add(p)
			user.save()
		return user