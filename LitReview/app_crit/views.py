from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import time
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

def indexReview(request,id):
     ticketReview = Ticket.objects.get(id=id)   # obtenir l'enregistrement(objet) du modele Ticket ayant comme id,
                                                # l'id récupéré dans le html avec request
                                                # inst_ticket_other_user_whithout_review.id

     form = ReviewForm(request.POST or None)
     messages = "enregistrement ok"
     # Recup de tous les Reviews de l'utilisateur connecté
     reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)

    #*************************************
     if form.is_valid() :
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticketReview
            review.save()
            return redirect('posts')
    #*************************************
     ''''
     # Mise de l'utilisateur
     if form.is_valid():
        donneesFormulaireReview = form.save(commit=False)
        donneesFormulaireReview.user = request.user
        form.save()
        form = ReviewForm()
     else :
         messages = "Enregistrement"
     '''

     context = {
         'form': form,
         'messages': messages,
         'reviews_to_my_tickets': reviews_to_my_tickets,
         'ticketReview': ticketReview,
     }
     return render(request, 'creatReview.html', context=context )


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
    form = UserFollowsForm(request.POST or None)

    obj_recup_01 = "test objet recup 1"
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

@login_required
def viewsPosts(request):
    # récup de tous les Reviews et tous les tickets, mais uniquement de l'utilisateur connecté
    reviews_user = Review.objects.filter(user=request.user)
    tickets_user = Ticket.objects.filter(user=request.user)

    # liste de tickets dans tous mes reviews
    listTicketInReviews_user = []
    # liste de tous mes tickets
    listTicketInTicket_user = []
    # liste de tickets qui ne sont pas dans les Reviews
    listTicketWithoutReviews_user = []
    listTicket_user = []
    listReview_user = []

    # liste de tous les Reviews utilisateur
    for i in reviews_user:
        listReview_user.append(i)

    # liste de tous les Reviews
    allReviews = Review.objects.all()

    # Création de la liste de tous les tickets dans Review de l'utilisateur
    for ticketReview in reviews_user:
        ticketInReview_user = ticketReview.ticket.id
        listTicketInReviews_user.append(ticketInReview_user)

    # Création de la liste de tous les id (tickets) dans ticket de l'utilisateur
    for idTicket in tickets_user:
        TicketInTicket_user = idTicket.id
        listTicketInTicket_user.append(TicketInTicket_user)
        listTicket_user.append(TicketInTicket_user)

    # Création de la liste des tickets ayant comme Review lui-même
    listTicketReviewsEvenUser=[]
    for i in reviews_user:
        if i.ticket.user == i.user:
           listTicketReviewsEvenUser.append(i.ticket.id)

    # CONSTRUCTION DE LA LISTE DES TICKETS QUI N'ONT PAS DE REVIEW (à partir des 2 listes précédentes)
    # on prend la liste de tous les tickets, et on supprime ceux qui se retrouvent dans review avec pop
    # copie de la liste des tickets utilisateurs dans la liste pour construction liste ticket sans review
    listTicketWithoutReviews_user = [i for i in listTicketInTicket_user]

    # La 1ere boucle teste tous les tickets en partant du dernier de la liste jusqu'au ticket avec index = 0
    longListTicket = len(listTicketInTicket_user)
    longListTicketx = len(listTicketInTicket_user)
    # pour tous les tickets en partant de la fin de la liste jusqu'au ticket [0]
    while longListTicket >= 1:
        indexTicketListe = longListTicket - 1
        idTicketTicket = listTicketInTicket_user[indexTicketListe]
        # La 2eme boucle teste tous les tickets des Reviews, et vérifie que l'id du ticket ne se trouve pas
        # dans le Review testé. Si le ticket est dans un Review, il est supprimé de la liste,
        # à la fin des boucles, ne resteront que les tickets sans Review
        indexReview = 0
        for j in listTicketInReviews_user:
            # boucleFor_nbr_review += 1
            idTicketInReview = listTicketInReviews_user[indexReview]
            if str(idTicketTicket) == str(idTicketInReview):
                listTicketWithoutReviews_user.pop(indexTicketListe)
                break
            indexReview += 1
        longListTicket -= 1

    # Récupération des tickets uniquement des autres utilisateurs pour le HTML
    # récupérer tous les tickets et exclure ceux de l'utilisateur
    tickets_other_user_0 = Ticket.objects.all()
    tickets_other_user = tickets_other_user_0.exclude(user=request.user)

    if request.method == 'POST' and "name_post_review_bouton_supprimer" in request.POST:
        review = get_instance(request, models.Review, review_id)
        return render(request, 'review_delete.html', context=context)

    if request.method == 'POST' and "name_post_review_bouton_modifier" in request.POST:
        review = get_instance(request, models.Review, review_id)
        return render(request, 'review_update.html', context=context)

    # chain transforme les 2 dict en un, ce qui permettra d'utiliser une seule itération pour les 2 dans le HTML
    tickets_and_reviews = sorted(
        chain(tickets_user, reviews_user),
        key=lambda instance: instance.time_created,
        reverse=True)

    list_for_max_star = [1, 2, 3, 4, 5]

    context = {
        'reviews_user': reviews_user,
        'tickets_user': tickets_user,
        'tickets_and_reviews': tickets_and_reviews,
        'tickets_other_user': tickets_other_user,
        'allReviews': allReviews,
        'listTicketInReviews_user': listTicketInReviews_user,
        'listTicketInTicket_user': listTicketInTicket_user,
        'listTicketWithoutReviews_user': listTicketWithoutReviews_user,
        'listTicket_user': listTicket_user,
        'list_for_max_star': list_for_max_star,
        'listTicketReviewsEvenUser':listTicketReviewsEvenUser,
    }
    return render(request, 'posts.html', context=context)

@login_required
def viewsFlux(request):

    # récup de tous les Reviews de l'utilisateur et de tous les utilisateurs
    test = request.user
    reviews_user = Review.objects.filter(user=test)
    #reviews_user = Review.objects.filter(user=request.user)
    reviews_all_user = Review.objects.all()
    list_reviews_user =[]
    # CREATION DE LA LISTE DES REVIEWS AUTRES UTILISATEURS
    # création liste review utilisateur
    for i in reviews_user:
        list_reviews_user.append(i.id)

    list_reviews_all_user =[]
    # création liste review
    for i in reviews_all_user:
        list_reviews_all_user.append(i.id)

    # création liste de tous les tickets
    ticket_all_user = Ticket.objects.all()
    list_ticket_all_user = []
    for i in ticket_all_user:
        list_ticket_all_user.append(i.id)

    # création liste des tickets utilisateurs
    ticket_user = Ticket.objects.filter(user=request.user)
    list_ticket_user = []
    for i in ticket_user:
        list_ticket_user.append(i.id)

    # création liste ticket de tous les reviews
    list_ticket_all_user_all_review = []
    for ticketReview_all_user in reviews_all_user:
        ticketInReview_all_user = ticketReview_all_user.ticket.id
        list_ticket_all_user_all_review.append(ticketInReview_all_user)

    # Création de la liste des reviews autres utilisateurs à partir de la liste de tous les review
    list_reviews_other_user = [i for i in list_reviews_all_user]
    longListReview = len(list_reviews_all_user)
    while longListReview >= 0:
        indexReview = longListReview - 1
        index2 = 0
        for j in list_reviews_user:
            if list_reviews_all_user[indexReview] == list_reviews_user[index2]:
                list_reviews_other_user.pop(indexReview)
                break
            index2 += 1
        longListReview -= 1

    # Création de la liste des tickets autres utilisateurs à partir de la liste de tous les tickets
    list_ticket_other_user = [i for i in list_ticket_all_user]
    longListTicket = len(list_ticket_all_user)
    while longListTicket >= 0:
        indexTicket = longListTicket - 1
        index2 = 0
        for j in list_ticket_user:
            if list_ticket_all_user[indexTicket] == list_ticket_user[index2]:
               list_ticket_other_user.pop(indexTicket)
               break
            index2 += 1
        longListTicket -= 1

    # CREATION DE LA LISTE DES TICKETS AUTRES UTILISATEURS SANS REVIEW ENSUITE
    # TESTER TOUS LES TICKETS UTILISATEURS ET VERIFIER SI DANS REVIEWS
    list_ticket_other_user_whithout_review = [i for i in list_ticket_other_user]

    longListTicket_other_user = len(list_ticket_other_user)

    while longListTicket_other_user >= 0:
        indexTicket_other_user = longListTicket_other_user - 1
        index2 = 0
        for j in list_reviews_all_user:
            if list_ticket_other_user[indexTicket_other_user] == list_ticket_all_user_all_review[index2]:
                list_ticket_other_user_whithout_review.pop(indexTicket_other_user)
                break
            index2 += 1
        longListTicket_other_user = longListTicket_other_user - 1

    ticket_other_user_whithout_review =[]
    for i in list_ticket_other_user_whithout_review:
        for j in ticket_all_user:
            if i == j.id:
                ticket_other_user_whithout_review.append(j)

    # récup de tous les tickets de l'utilisateur et de tous les utilisateurs
    tickets_user = Ticket.objects.filter(user=request.user)
    tickets_all_user = Ticket.objects.all()

    reviews_other_user_0 = Review.objects.all()
    reviews_other_user = reviews_other_user_0.exclude(user=request.user)


    Ticket_id = ticket_all_user
    userFollow = UserFollows.objects.filter(user=request.user)

    # liste des utilisateurs que je suis
    listUserFollow=[]
    for i in userFollow:
        listUserFollow.append(i.followed_user)

    # Créer une liste des tickets autre utilisateurs sans review suivis
    listTicketOtherUserFollowed = []
    listI = []
    listJ=[]
    for i in ticket_other_user_whithout_review:
        for j in listUserFollow:
            if i.user == j:
                listTicketOtherUserFollowed.append(j)
            listI.append(i.user)
            listJ.append(j)

    if request.method == 'POST' and "nameFluxCreatReviewTicketConnu" in request.POST:
        Ticket_id = ticket_all_user
        userFollow = UserFollows.objects.all()
        context={
            'Ticket_id': Ticket_id,
            'listUserFollow': listUserFollow,
            'listTicketOtherUserFollowed': listTicketOtherUserFollowed,
        }
        return render(request, 'creatTicketReview.html', context=context)


    tickets_and_reviews = sorted(chain(tickets_all_user, reviews_all_user),
        key=lambda instance: instance.time_created,
        reverse=True)

    list_for_max_star = [1, 2, 3, 4, 5]

    context = {
        'tickets_and_reviews': tickets_and_reviews,
        'reviews_all_user': reviews_all_user,
        'reviews_user': reviews_user,
        'reviews_other_user_0': reviews_other_user_0,
        'reviews_other_user': reviews_other_user,
        'listTicketOtherUserFollowed':listTicketOtherUserFollowed,
        'tickets_all_user': tickets_all_user,
        'tickets_user': tickets_user,
        'ticket_other_user_whithout_review': ticket_other_user_whithout_review,
        'listUserFollow': listUserFollow,
        'userFollow': userFollow,
        'Ticket_id': Ticket_id,
        'list_reviews_all_user': list_reviews_all_user,
        'list_reviews_user': list_reviews_user,
        'list_reviews_other_user': list_reviews_other_user,
        'list_ticket_other_user': list_ticket_other_user,
        'list_ticket_other_user_whithout_review': list_ticket_other_user_whithout_review,
        'list_ticket_all_user_all_review': list_ticket_all_user_all_review,
        'list_for_max_star': list_for_max_star,
    }
    return render(request, 'flux.html', context=context) # le formulaire est généré dans le modèle


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

'''
def creatReviewTicketConnu(request):
     review_form = ReviewForm()
     ticket_form = TicketForm()
     # si click
     if request.method == 'POST' or None and "nameFluxCreatReviewTicketConnu" in request.POST:
         ticket_form = TicketForm(request.POST, request.FILES)
         review_form = ReviewForm(request.POST)
         ticket_id = ticket_form.id

         if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket_id
            ticket.save()
            review.save()
         return redirect('home')

     context = {
         'review_form': review_form,
     }
     return render (request, 'CreatReviewTicketConnu.html', context=context)
'''
