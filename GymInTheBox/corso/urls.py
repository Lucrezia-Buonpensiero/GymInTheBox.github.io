from django.urls import path
from . import views

app_name = 'corso'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index_corsi'),
    #sistemare
    path('<int:id>/', views.dettaglio_corso, name='dettaglio_corso'),
    path('<int:id>/prenotazione/', views.prenotazione_corso, name='prenotazione_corso'),
    path('<int:id>/cancella_prenotazione/', views.cancella_prenotazione, name='cancella_prenotazione'),
    path('aggiungi_corso/', views.aggiungi_corso, name='aggiungi_corso'),
    path('<int:id>/modifica_corso/', views.modifica_corso, name='modifica_corso'),
    path('<int:id>/cancella_corso', views.cancella_corso, name='cancella_corso'),
]