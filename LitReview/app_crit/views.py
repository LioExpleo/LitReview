from django.shortcuts import render

# Create your views here.
# importer les modèles
from .models import Ticket, Review, UserFollows

# importer la classe du formulaire
from .formulaire import TicketForm, ReviewForm, UserFollowsForm, Abonnement

# Pour créer le formulaire, faire l'instanciation sur la classe du formulaire importé ReviewForm
# indiquer le formulaire sous forme d'un dictionnaire avec {}

# Ecrire une fonction qui va,
# Définir la classe qui va permettre de générer le formulaire en la faisant dériver de ModelForm
# et en lui spécifiant le modèle à inclure


def indexTicket(request):
     form = TicketForm(request.POST or None, request.FILES)
     messages = "enregistrement ok"
     if form.is_valid():
        form.save()
        form = TicketForm()
     return render(request, 'indexTicket.html', {'form': form, 'message': messages} )

def indexReview(request):
     form = ReviewForm(request.POST or None)
     messages = "enregistrement ok"
     if form.is_valid():
        form.save()
        form = ReviewForm()
     return render(request, 'indexReview.html', {'form': form, 'message': messages} )

def indexUserFollows(request):
     form = UserFollowsForm(request.POST or None)
     messages = "enregistrement ok"
     if form.is_valid():
        form.save()
        form = UserFollowsForm()
     return render(request, 'indexUserFollows.html', {'form': form, 'message': messages} )


def indexAbonnement(request):
    """
    Management function of the followed users page
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
            #form = service_subscription(request)
        else:
            pass
            #form = SubsriptionForm()
        #context = {
         #   'form': form,
         #   'followed': service_followed_users(request)
        #}
        #return render(request,"indexAbonnement.html",context)
    #return redirect('userlogin')
    pass
    return()


