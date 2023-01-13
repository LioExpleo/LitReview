from django.forms import ModelForm
from .models import Ticket, Review, UserFollows

class TicketForm(ModelForm):
    # Une class meta est une classe qui utilise une classe, cela va indiquer à django quelle classe utiliser
    # pour le formulaire

    # Le modèle Ticket doit être utilisé pour créer le formulaire
    # Précision des champs uniquement utiles du modèle à utiliser dans le formulaire ensuite
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', 'user']
        enctype = "multipart/form-data"




        """
         'image': forms.TextInput(
                attrs={
                    'class': 'ticket_body__form__form',
                    'placeholder': "facultatif, lien URL uniquement."
                }
            )
        """

class ReviewForm(ModelForm):
    # Une class meta est une classe qui utilise une classe, cela va indiquer à django quelle classe utiliser
    # pour le formulaire

    # Le modèle Review doit être utilisé pour créer le formulaire
    # Précision des champs uniquement utiles du modèle à utiliser dans le formulaire ensuite
    class Meta:
        model = Review
        fields = ['ticket','rating', 'user', 'headline', 'body']
        enctype = "multipart/form-data"

class UserFollowsForm(ModelForm):
    # Une class meta est une classe qui utilise une classe, cela va indiquer à django quelle classe utiliser
    # pour le formulaire

    # Le modèle UserFollows doit être utilisé pour créer le formulaire
    # Précision des champs uniquement utiles du modèle à utiliser dans le formulaire ensuite
    class Meta:
        model = UserFollows
        fields = ['user', 'followed_user']
        enctype = "multipart/form-data"
