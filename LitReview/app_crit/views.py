from django.shortcuts import render

# Create your views here.
# importer les modèles
from .models import Ticket, Review, UserFollows


# importer la classe du formulaire
from .formulaire import TicketForm, ReviewForm, UserFollowsForm

from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth.models import User

# Pour créer le formulaire, faire l'instanciation sur la classe du formulaire importé ReviewForm
# indiquer le formulaire sous forme d'un dictionnaire avec {}

# Ecrire une fonction qui va,
# Définir la classe qui va permettre de générer le formulaire en la faisant dériver de ModelForm
# et en lui spécifiant le modèle à inclure


def indexTicket(request):
     form = TicketForm(request.POST or None, request.FILES) #
     messages = "enregistrement"
     if form.is_valid():
        form.save()
        form = TicketForm()

     return render(request, 'indexTicket.html', {'form': form}) #, 'message': messages

def indexReview(request):
     form = ReviewForm(request.POST or None)
     messages = "enregistrement ok"
     reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)
     if form.is_valid():
        form.save()
        form = ReviewForm()
     else :
         messages = "Enregistrement"
     return render(request, 'indexReview.html', {'form': form, 'messages': messages, 'reviews_to_my_tickets': reviews_to_my_tickets} )


def indexUserFollows(request):
     form = UserFollowsForm(request.POST or None)
     messages = "enregistrement ok"
     reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)

     Test= "test var"
     obj_recup_01 = "test objet recup 1"

     if form.is_valid():
        form.save()
        form = UserFollowsForm()
     return render(request, 'indexUserFollows.html', {'form': form, 'message': messages, 'reviews_to_my_tickets': reviews_to_my_tickets, 'Test': Test,  'obj_recup_01': obj_recup_01} )



def indexAbonnement(request):
    """
    Management function of the followed users page
    """
    form = UserFollowsForm(request.POST or None)

    obj_recup_01 = "test objet recup 1"

    #if request.user.is_authenticated:
    obj_recup_01 = "test objet recup 1"
    obj_recup_01 = Review.objects.filter(ticket__user_id=request.user.id)
    obj_recup_01 = Review.objects.all()

    #obj_recup_01 = Ticket.objects.filter(Title='Title 21012023')
    obj_recup_00 = Review.objects.all()
    obj_recup_01 = Review.objects.filter(user_id=2)
    obj_recup_02 = Review.objects.filter(rating=2)
    obj_recup_03 = Review.objects.values("rating")
    obj_recup_04 = Review.objects.all()
    obj_recup_05 = Review.objects.all()
    obj_recup_06 = UserFollows.objects.values("user")
    obj_recup_07 = UserFollows.objects.values("followed_user")

    #obj_recup_04 = UserFollows.objects.filter(user=user)
    #obj_recup_05 = UserFollows.objects.filter(followed_user=user)
    #obj_recup_06 = Review.objects.filter(user__id__in=followed_user)
    #obj_recup_07 = Ticket.annotate(content_type=Value('TICKET', CharField()))

    '''
    def hello(request):
    bands = Band.objects.all()
    return HttpResponse(f”””
        <html>
            <head><title>Merchex</title><head>
            <body>
                <h1>Hello Django !</h1>
                <p>Mes groupes préférés sont :<p>
                <ul>
                    <li>{bands[0].name}</li>
                    <li>{bands[1].name}</li>
                    <li>{bands[2].name}</li>
                </ul>
            </body>
        </html>
    ”””)
    '''

    # templateAbonnement.html
    if form.is_valid():
        form.save()
        form = UserFollowsForm()
    return render(request, 'templateAbonnement.html', {'form': form, 'obj_recup_01': obj_recup_01, 'obj_recup_02': obj_recup_02, 'obj_recup_03': obj_recup_03, 'obj_recup_04': obj_recup_04, 'obj_recup_05': obj_recup_05, 'obj_recup_06': obj_recup_06, 'obj_recup_07': obj_recup_07} )


    # reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)
    #obj_recup_01 = Reviews.objects.get(name='Description')

    #obj_recup_02 = Reviews.objects.get(name='Description')
    #obj_recup_03 = Reviews.objects.get(name='Description')
    #reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)

    #return(render(request, 'indexUserFollows.html', context={ "obj_recup_01": obj_recup_01 }))
    #X = UserFollows.followed_user.objects.filter(UserFollows.id=request.user.id)

    #context = { indexReview()}

