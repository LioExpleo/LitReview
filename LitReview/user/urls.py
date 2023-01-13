from django.urls import path, include
from django.contrib.auth import views as auth_views
# from .views import register
from .views import home, register

urlpatterns =[path('',home, name='home'),
              path('accounts/', include('django.contrib.auth.urls')),
              path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
              path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
             path('register/', register, name='register'),
               ]
'''
path('register/', register, name='register'),


# path('accounts/', include('django.contrib.auth.urls') ajoute
accounts/ login/ [name='login']
accounts/ logout/ [name='logout']
accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']
accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete']
'''

'''
path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name = 'login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name = 'logout'),
	path('register/', views.register, name='register'),
'''
