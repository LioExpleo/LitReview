from .views import indexTicket, indexReview, indexUserFollows

from .views import indexReview, indexTicket, indexUserFollows
from django.urls import path

# 1 nom affiché dans l'adresse navigateur
# 2 def views
# 3 html
urlpatterns = [path('CreatTicket/', indexTicket, name='indexTicket'),
               path('CreatReview/', indexReview, name='indexReview'),
               path('CreatUserFollows/', indexUserFollows, name='indexUserFollows'),

              ]
