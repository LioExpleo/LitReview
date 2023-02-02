from .views import indexTicket, indexReview, indexUserFollows

from .views import indexReview, indexTicket, indexUserFollows, indexAbonnement
from django.urls import path

# 1 nom affiché dans l'adresse navigateur
# 2 def views
# 3 html
urlpatterns = [path('CreatTicket/', indexTicket, name='creatTicket'),
               path('CreatReview/', indexReview, name='creatReview'),
               path('CreatUserFollows/', indexUserFollows, name='abonnement'),

               path('CreatAbonnement/', indexAbonnement, name='indexAbonnement'),
              ]
