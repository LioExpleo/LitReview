from .views import indexTicket, indexReview, indexTicketReview, indexUserFollows, indexAbonnement, viewsPosts, review_update, review_delete
from django.urls import path

# 1 nom affiché dans l'adresse navigateur
# 2 def views
# 3 html
urlpatterns = [path('CreatTicketReview/', indexTicketReview, name='creatTicketReview'),
               path('CreatTicket/', indexTicket, name='creatTicket'),
               path('CreatReview/', indexReview, name='creatReview'),
               path('CreatUserFollows/', indexUserFollows, name='abonnement'),

               path('posts/', viewsPosts, name='posts'),



               path("<int:id>/review_delete/", review_delete, name='review_delete'),
               path("<int:id>/review_update/", review_update, name='review_update'),
               # path("<int: x.id> review_delete/", review_delete, name='review_delete'),
               # path('posts/ticket<int:ticket_id>/edit/', blog.views.ticket_edit, name='ticket_edit'),
               # path('posts/ticket<int:ticket_id>/delete/', blog.views.ticket_delete, name='ticket_delete'),
               # path('posts/review<int:review_id>/edit/', blog.views.review_edit, name='review_edit'),
               # path('reviewDelete/', viewsPosts, name='posts'),
               # path('posts/review<int:review_id>/delete/', review_delete, name='review_delete'),
               # path('posts/', viewsPosts, name='review_delete'),



               path('CreatAbonnement/', indexAbonnement, name='indexAbonnement'),
              ]
