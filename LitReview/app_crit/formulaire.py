from django.forms import ModelForm
from .models import Ticket, Review, UserFollows
from django import forms

from .forms_settings import (
    CHOICES_REVIEW_FORM
)

class TicketForm(ModelForm):
    # Une class meta est une classe qui utilise une classe, cela va indiquer à django quelle classe utiliser
    # pour le formulaire

    # Le modèle Ticket doit être utilisé pour créer le formulaire
    # Précision des champs uniquement utiles du modèle à utiliser dans le formulaire ensuite

    class Meta:
        model = Ticket

        #exclude = ['user']
        #exclude = ['image']

        fields = ['title', 'description', 'image']

        #enctype = "multipart/form-data"

        labels = {"title": "", "description": "", "image": "" }

        widgets = {
                'title': forms.TextInput(
                    attrs={
                        'class': 'cl_ticket_form_title'
                    }
                ),
                'description': forms.Textarea(
                    attrs={
                        'class': 'cl_ticket_form_description'
                    }
                ),
            }

class ReviewForm(ModelForm):
    # Une class meta est une classe qui utilise une classe, cela va indiquer à django quelle classe utiliser
    # pour le formulaire
    # Le modèle Review doit être utilisé pour créer le formulaire
    # Précision des champs uniquement utiles du modèle à utiliser dans le formulaire ensuite
    rating = forms.IntegerField(
        widget=forms.RadioSelect(
            choices=((i, i) for i in range(0, 6))
        )
    )
    class Meta:
        model = Review

        fields = ['rating', 'headline', 'body']
        # enctype = "multipart/form-data"

        widgets ={
                'headline': forms.TextInput(
                attrs={
                    'class': 'review_form_headline'
                }
                ),
                'body': forms.Textarea(
                attrs={
                    'class': 'review_form_body'
                }
                ),

        }
'''
 'rating': forms.RadioSelect(
                choices=CHOICES_REVIEW_FORM,
                attrs={
                    'class': 'review_form_rating'
                }
            ),
'''
class UserFollowsForm(ModelForm):
    # Une class meta est une classe qui utilise une classe, cela va indiquer à django quelle classe utiliser
    # pour le formulaire

    # Le modèle UserFollows doit être utilisé pour créer le formulaire
    # Précision des champs uniquement utiles du modèle à utiliser dans le formulaire ensuite.
    class Meta:
        model = UserFollows
        fields = ['followed_user']
        enctype = "multipart/form-data"

        labels = {"followed_user": "followed_user" }

# blog/models.py
from django.conf import settings
from django.db import models


class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)


