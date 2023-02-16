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

from itertools import chain
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
        # obtenir les donnees, de modele dans le cas précis mais pas obligatoirement,  a partir d'un formulaire
        # afin de remplir certains champs
        # dans les donnees formulees du formulaire. Ici, user doit être indiqué car dans le formulaire,
        # mais il n'est pas dans les champs du formulaire ensuite.
        donneesFormulaireTicket = form.save(commit=False)
        donneesFormulaireTicket.user = request.user
        #donneesFormulaireTicket.image = "https://www.bing.com/maps?q=projet+9+d%C3%A9vellopeur+application+python+guithub&FORM=HDRSC4&cp=46.780342%7E-1.402078&lvl=12.1"
        form.save()
        form = TicketForm()
     return render(request, 'creatTicket.html', {'form': form, 'messages': messages, 'obj_recup_01': obj_recup_01})

def indexReview(request):
     form = ReviewForm(request.POST or None)
     messages = "enregistrement ok"
     # Recup de tous les Reviews de l'utilisateur connecté
     reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)


     # Mise de l'utilisateur
     if form.is_valid():
        donneesFormulaireReview = form.save(commit=False)
        donneesFormulaireReview.user = request.user
        form.save()
        form = ReviewForm()
     else :
         messages = "Enregistrement"
     return render(request, 'creatReview.html', {'form': form, 'messages': messages, 'reviews_to_my_tickets': reviews_to_my_tickets} )


        # obtenir les donnees de modele a partir d'un formulaire afin de remplir certains champs
        # dans les donnees formulees du formulaire. Ici, user doit être indiqué car dans le modèle,
        # mais il n'est pas dans le formulaire.
        # donneesFormulaireTicket = form.save(commit=False)
        #donneesFormulaireTicket.user = request.user
        #donneesFormulaireTicket.image = "https://www.bing.com/maps?q=projet+9+d%C3%A9vellopeur+application+python+guithub&FORM=HDRSC4&cp=46.780342%7E-1.402078&lvl=12.1"
        #form.save()
        #form = TicketForm()

        #return render(request, 'creatTicketReview.html', {'form': form, 'messages': messages, 'obj_recup_01': obj_recup_01})


def indexTicketReview(request):
     review_form = ReviewForm()
     ticket_form = TicketForm()
     # si click
     if request.method == 'POST' or None and "name_ticketReview_bouton_envoyer" in request.POST:
         ticket_form = TicketForm(request.POST, request.FILES)
         review_form = ReviewForm(request.POST)
         if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.is_reviewed = True
            ticket.user = request.user
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket

            ticket.save()
            review.save()
         return redirect('home')

     context = {
         'ticket_form': ticket_form,
         'review_form': review_form,
     }
     return render (request, 'creatTicketReview.html', context=context)

@login_required
def indexUserFollows(request):
     form = UserFollowsForm(request.POST or None, request.FILES)
     obj_recup_01 = request.user.username
     obj_recup_02 = "******************** Aide saisie *******************"
     boutonVue = 0
     # abonnement avec click sur bouton "ENVOYER" dans html
     # si requete est post avec le bouton envoyer
     if request.method == 'POST' and "name_bouton_envoyer" in request.POST:
        form = UserFollowsForm(request.POST or None, request.FILES)

        # obtenir les donnees de forms qui n'ont pas été mises dans le formulaire afin d'y mettre des valeurs
        # Ici, user doit être indiqué car dans le modèle, et donc dans form issu du modèle
        # mais il n'est pas dans le formulaire, il faut donc le renseigner avec request.user.
        donneesFormulaire = form.save(commit=False)
        donneesFormulaire.user = request.user
        followedUserSelect = donneesFormulaire.followed_user
        # si l'utilisateur sélectionné pour le suivi est différent de l'utilisateur connecté
        if followedUserSelect != donneesFormulaire.user:
            if form.is_valid():
                try:
                    form.save()
                    form = UserFollowsForm()
                    obj_recup_02 = " " + str(donneesFormulaire.followed_user) + \
                                   " ajouté dans les utilisateurs suivis"
                except:
                    obj_recup_02 = " " + str(donneesFormulaire.followed_user) + \
                                   " non sélectionnable, vérifier daans liste si déjà suivi"
        # si l'utilisateur sélectionné pour le suivi est l'utilisateur connecté
        else :
            obj_recup_02 = "L'utilisateur" + str(donneesFormulaire.user) + " connecté ne peut se suivre lui-même"

     # désabonnement avec click sur bouton "se désabonner" dans html
     if request.method == 'POST' and "name_bouton_desabonner" in request.POST:
        form = UserFollowsForm(request.POST or None, request.FILES)
        instance = UserFollows.objects.get(user=request.user, followed_user=request.POST['name_bouton_desabonner'])
        obj_recup_02 = instance.followed_user
        instance.delete()
        obj_recup_02 = "utilisateur " + str(obj_recup_02) + " vient d'être désabonné"
     return render(request, 'abonnement.html', {'form': form, 'obj_recup_01': obj_recup_01, 'obj_recup_02': obj_recup_02})

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
    # obj_recup_01 = Reviews.objects.get(name='Description')

    #obj_recup_02 = Reviews.objects.get(name='Description')
    #obj_recup_03 = Reviews.objects.get(name='Description')
    #reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)

    # return(render(request, 'abonnement.html', context={ "obj_recup_01": obj_recup_01 }))
    # X = UserFollows.followed_user.objects.filter(UserFollows.id=request.user.id)

    # context = { indexReview()}
import copy
#@login_required
def viewsPosts(request):
    reviews_user = Review.objects.filter(user=request.user)
    tickets_user = Ticket.objects.filter(user=request.user)

    # liste de tickets dans tous mes reviews
    listTicketInReviews_user = []
    listTicketInTicket_user = []
    listTicketWithoutReviews_user = []
    supPop=''

    allReviews = Review.objects.all()
    # liste de tous les tickets dans Review de l'utilisateur, pas tous les reviews
    for ticketReview in reviews_user:
        ticketInReview_user = ticketReview.ticket.id
        listTicketInReviews_user.append(ticketInReview_user)

    # liste de tous les id (tickets) dans ticket de l'utilisateur
    for idTicket in tickets_user:
        x = idTicket.id
        listTicketInTicket_user.append(x)

    # liste de tous les tickets qui n'ont pas de review utilisateur
    # on prend la liste de tous les tickets, et on supprime ceux qui se retrouvent dans review avec pop
    # avec = les 2 listes sont liées
    listTicketInTicket_user_pour_html = [i for i in listTicketInTicket_user]
    listTicketWithoutReviews_user = listTicketInTicket_user
    #listTicketWithoutReviews_user = [i for i in listTicketInTicket_user]
    index1 = 0
    for x in listTicketInTicket_user:

        idTicketTicket = listTicketInTicket_user[index1]
        index2 = 0
        for y in listTicketInReviews_user:
            idTicketInReview = listTicketInReviews_user[index2]
            if idTicketTicket == idTicketInReview:
                listTicketWithoutReviews_user.pop(index1)
            index2 += 1
        index1 += 1


    #tickets_user_whithout_review = tickets_user

    tickets_other_user_0 = Ticket.objects.all()
    tickets_other_user = tickets_other_user_0.exclude(user=request.user)

    if request.method == 'POST' and "name_post_review_bouton_supprimer" in request.POST:
        review = get_instance(request, models.Review, review_id)
        return render(request, 'review_delete.html', context=context)

    if request.method == 'POST' and "name_post_review_bouton_modifier" in request.POST:
        review = get_instance(request, models.Review, review_id)
        return render(request, 'review_update.html', context=context)

    # chain transforme les 2 dict en un, ce qui permettra d'itérer sur les 2 de façon non séparée

    tickets_and_reviews = sorted(
        chain(tickets_user, reviews_user),
        key=lambda instance: instance.time_created,
        reverse=True)

    context = {
        'reviews_user': reviews_user,
        'tickets_user': tickets_user,
        'tickets_and_reviews': tickets_and_reviews,
        'tickets_other_user': tickets_other_user,
        'allReviews': allReviews,
        'listTicketInReviews_user': listTicketInReviews_user,
        'listTicketInTicket_user': listTicketInTicket_user,
        'listTicketWithoutReviews_user': listTicketWithoutReviews_user,
        'listTicketInTicket_user_pour_html': listTicketInTicket_user_pour_html,
    }
    return render(request, 'posts.html', context=context)



@login_required
def review_delete(request, id):
    review = Review.objects.get(id= id)

    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 'review_delete.html', {'review': review})


# Création de la vue update
@login_required
def review_update(request, id):
    review = Review.objects.get(id=id)
    form = ReviewForm(instance=review)  # rempli le formulaire avec
                                        # les valeurs existantes correspondant à l'enregistrement
    reviewTicket = review.ticket
    reviewRating = review.rating
    reviewHeadline = review.headline
    reviewBody = review.body
    reviewRating_0=10
    reviewRating_1=11
    reviewRating_2=12
    reviewRating_3=13
    reviewRating_4=14
    reviewRating_5=15


    #form = ReviewForm(request.POST, instance=review)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save() # force_update=True
            return redirect('posts')
        else:
            form = ReviewForm(instance=review)

        #return render(request, 'review_update.html', {'form': form}) # le formulaire est généré dans le modèle
    context = {
        'form': form,
        'reviewTicket': reviewTicket,
        'reviewRating': reviewRating,
        'reviewHeadline': reviewHeadline,
        'reviewBody': reviewBody,
        'reviewRating_0': reviewRating_0,
        'reviewRating_1': reviewRating_1,
        'reviewRating_2': reviewRating_2,
        'reviewRating_3': reviewRating_3,
        'reviewRating_4': reviewRating_4,
        'reviewRating_5': reviewRating_5,
    }
    return render(request, 'review_update.html', context=context) # le formulaire est généré dans le modèle

@login_required
def ticket_delete(request, id):
    ticket = Ticket.objects.get(id= id)

    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'ticket_delete.html', {'ticket': ticket})

@login_required
def ticket_update(request, id):
    ticket = Ticket.objects.get(id=id)
    form = TicketForm(instance=ticket)  # rempli le formulaire avec
                                        # les valeurs existantes correspondant à l'enregistrement
    ticketTitle = ticket.title

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket,)
        if form.is_valid():
            form.save() # force_update=True
            return redirect('posts')
        else:
            form = TicketForm(instance=ticket)

        #return render(request, 'review_update.html', {'form': form}) # le formulaire est généré dans le modèle
    context = {
        'form': form,
        'ticketTitle': ticketTitle,
    }
    return render(request, 'ticket_update.html', context=context) # le formulaire est généré dans le modèle


