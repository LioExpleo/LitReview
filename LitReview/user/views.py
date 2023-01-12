from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def register(request):
	if request.method == 'POST' :
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
			return redirect('home')
	else :
		form = UserCreationForm()
	return render(request,'registration/register.html',{'form' : form})
from django.shortcuts import render


