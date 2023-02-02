from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
# importer les modèles
from .models import Ticket, Review, UserFollows
from django.contrib.auth.models import User

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
     messages = request.user.username

     obj_recup_01 = request.user.username
     if form.is_valid():
        # obtenir les donnees de modele a partir d'un formulaire afin de remplir certains champs
        # dans les donnees formulees du formulaire. Ici, user doit être indiqué car dans le modèle,
        # mais il n'est pas dans le formulaire.
        donneesFormulaireTicket = form.save(commit=False)
        donneesFormulaireTicket.user = request.user
        #donneesFormulaireTicket.image = "https://www.bing.com/maps?q=projet+9+d%C3%A9vellopeur+application+python+guithub&FORM=HDRSC4&cp=46.780342%7E-1.402078&lvl=12.1"
        form.save()
        form = TicketForm()
     return render(request, 'creatTicket.html', {'form': form, 'messages': messages, 'obj_recup_01': obj_recup_01})

def indexReview(request):
     form = ReviewForm(request.POST or None)
     messages = "enregistrement ok"
     reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)
     if form.is_valid():
        form.save()
        form = ReviewForm()
     else :
         messages = "Enregistrement"
     return render(request, 'creatReview.html', {'form': form, 'messages': messages, 'reviews_to_my_tickets': reviews_to_my_tickets} )

@login_required
def indexUserFollows(request):
     form = UserFollowsForm(request.POST or None, request.FILES)
     obj_recup_01 = request.user.username
     obj_recup_02 = ""
     boutonVue = 0
     # abonnement avec click sur bouton "ENVOYER" dans html
     if request.method == 'POST' and "name_bouton_envoyer" in request.POST:
        form = UserFollowsForm(request.POST or None, request.FILES)

        # obtenir les donnees de forms qui n'ont pas été mises dans le formulaire afin d'y mettre des valeurs
        # Ici, user doit être indiqué car dans le modèle, et donc dans form issu du modèle
        # mais il n'est pas dans le formulaire.
        donneesFormulaire = form.save(commit=False)
        donneesFormulaire.user = request.user
        followedUserSelect = donneesFormulaire.followed_user

        if followedUserSelect != donneesFormulaire.user:
            if form.is_valid():
                try:
                    form.save()
                    form = UserFollowsForm()
                    obj_recup_02 = "Utilisateur " + str(donneesFormulaire.followed_user) + \
                                   " ajouté dans la liste des utilisateurs suivis"
                except:
                    obj_recup_02 = "Utilisateur " + str(donneesFormulaire.followed_user) + \
                                   " non selectionnable, vérifier si utilisateur n'est pas déjà suivi"
        else :
            obj_recup_02 = "l'utilisateur connecté ne peut se suivre lui-même"

     # désabonnement avec click sur bouton "se désabonner" dans html
     if request.method == 'POST' and "name_bouton_desabonner" in request.POST:
        form = UserFollowsForm(request.POST or None, request.FILES)
        instance = UserFollows.objects.get(user=request.user, followed_user=request.POST['name_bouton_desabonner'])
        obj_recup_02 = instance.followed_user
        instance.delete()
        obj_recup_02 = "utilisateur " + str(obj_recup_02) + " désabonné"

     return render(request, 'abonnement.html', {'form': form, 'obj_recup_01': obj_recup_01, 'obj_recup_02': obj_recup_02})


@login_required
def indexUserFollows2(request):
     form = UserFollowsForm(request.POST or None, request.FILES)

     # recup de l'utilisateur connecté
     obj_recup = request.user.username

     # Si le formulaire est valide
     if form.is_valid():
        # obtenir les donnees de forms qui n'ont pas été mises dans le formulaire afin d'y mettre des valeurs
        # Ici, user doit être indiqué car dans le modèle, et donc dans form issu du modele
        # mais il n'est pas dans le formulaire.

        donneesFormulaire = form.save(commit=False)
        donneesFormulaire.user = request.user
        form.save()
        form = UserFollowsForm()
     return render(request, 'extrait/extrCreatUserFollows.html', {'form': form, 'obj_recup': obj_recup})






















from app_crit.models import UserFollows
def indexAbonnement(request):
    #recup de tous les objets de la base de données

    #userFollow = UserFollows.objects.all()
    """
    Management function of the followed users page
    """

    form = UserFollowsForm(request.POST or None)

    obj_recup_01 = "test objet recup 1"

    #if request.user.is_authenticated:
    obj_recup_01 = "test objet recup 1"
    obj_recup_01 = Review.objects.filter(ticket__user_id=request.user.id)
    #obj_recup_01 = Review.objects.all()

    #obj_recup_01 = Ticket.objects.filter(Title='Title 21012023')
    obj_recup_00 = Review.objects.all()
    obj_recup_01 = Review.objects.filter(user_id=2)
    obj_recup_02 = Review.objects.filter(rating=2)
    obj_recup_03 = Review.objects.values("rating")

    obj_recup_04 = UserFollows.objects.values("user")
    obj_recup_04 = obj_recup_04[4]
    obj_recup_05 = UserFollows.objects.values("user", "followed_user")
    obj_recup_06 = UserFollows.objects.values("followed_user")
    obj_recup_07 = UserFollows.objects.values("user", "followed_user")

    #obj_recup_04 = UserFollows.objects.filter(user=user)
    #obj_recup_05 = UserFollows.objects.filter(followed_user=user)
    #obj_recup_06 = Review.objects.filter(user__id__in=followed_user)
    #obj_recup_07 = Ticket.annotate(content_type=Value('TICKET', CharField()))

    # templateAbonnement.html
    ''''''
    #user = UserFollows.objects.filter("user")
    userFollow = UserFollows.objects.all()

    if form.is_valid():
        form.save()
        form = UserFollowsForm()
    return render(request, 'templateAbonnement.html', {'form': form, 'obj_recup_01': obj_recup_01[0],
                                                       'obj_recup_02': obj_recup_02[0],
                                                       'obj_recup_03': obj_recup_03[0],
                                                       'obj_recup_04': obj_recup_04,
                                                       'obj_recup_05': obj_recup_05,
                                                       'obj_recup_06': obj_recup_06,
                                                       'obj_recup_07': obj_recup_07[2],
                                                       'userFollow': userFollow[6],
                                                       })

    # reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)
    #obj_recup_01 = Reviews.objects.get(name='Description')

    #obj_recup_02 = Reviews.objects.get(name='Description')
    #obj_recup_03 = Reviews.objects.get(name='Description')
    #reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)

    #return(render(request, 'abonnement.html', context={ "obj_recup_01": obj_recup_01 }))
    #X = UserFollows.followed_user.objects.filter(UserFollows.id=request.user.id)

    #context = { indexReview()}

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
