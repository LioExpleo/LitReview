from django.shortcuts import render, redirect
from .models import UserModel
from .models import UserModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


@login_required # fonction décorateur fournie par framework django, celle-ci

#Dans le cas présent nous utiliserons un décorateur d’authentification login_required
# qui va sécuriser et restreindre l’accès à la page d’accueil selon qu’un utilisateur est authentifiée ou non.

#si un utilisateur tente d’accéder à la page d’accueil pour la première fois, il sera automatiquement redirigé
# vers la page de connexion, dont l’url  LOGIN_URL est définie dans le fichier de configuration settings.py

def home(request):
	pass
	#context ={
	#'home': UserModel.objects.all()
	#}
	#return render(request, 'flux.html')
	return redirect('flux')

def register(request):
	if request.method == 'POST' :
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, f'Bienvenu {username}, Votre compte a été créé avec succès !')
			return redirect('flux')
	else:
		form = UserCreationForm()
	return render(request,'registration/register.html', {'form' : form})
