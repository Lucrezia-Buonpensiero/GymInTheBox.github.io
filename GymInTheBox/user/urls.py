from django.urls import path
from . import views
from django.contrib.auth import login
from django.contrib.auth import views as auth_views


app_name = 'user'
urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='template_user/login.html'), name='login'),
    path('logged_in/area_utente/', views.area_utente, name='area_utente'),
    path('registration/', views.Registration, name='registrazione'),
    path('logout/', views.Logout_view, name='logout_view'),
    path('contact_us/', views.contact , name='contact'),
    path('cancella_notifiche/', views.cancella_notifiche, name='cancella_notifiche'),
]