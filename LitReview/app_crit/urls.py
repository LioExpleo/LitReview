from .views import indexTicket, indexReview, indexUserFollows

from .views import indexReview, indexTicket, indexUserFollows
from django.urls import path

urlpatterns = [path('CreatTicket/', indexTicket, name='indexTicket'),
               path('CreatReview/', indexReview, name='indexReview'),
               path('CreatUserFollows/', indexUserFollows, name='indexUserFollows'),
              ]
