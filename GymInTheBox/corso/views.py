from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, Http404

from django.forms import ModelForm
from user.models import Tessera, Notifica
from django.contrib.auth.models import User
from . import models
from django.views import generic
from .models import Corso
from django.shortcuts import render
from .forms import FormCreazioneCorso

# Create your views here.
# ogni view deve ritornare un oggetto
# di tipo HttpResponse

#generic view per mostrare una lista di corsi
class IndexView(generic.ListView):
    template_name = 'template_corso/lista_corsi.html'
    context_object_name = 'lista_corsi'

    def get_queryset(self):
        return Corso.objects.all()

@login_required(login_url='/login/')
def dettaglio_corso(request, id):

    try:
        corso_sel = Corso.objects.get(pk=id)
    except Corso.DoesNotExist:
        return render(request, 'template_user/message.html', {'messaggio': "Spiacenti, Il corso non esiste più ):"})

    return render(request, 'template_corso/dettagli_corso.html', {'corso_sel': corso_sel} )

# Invio notifica quando si libera un posto
def notifica_utente(destinatario, corso):

    new_notifica = Notifica(user=destinatario, notifica="Sei stato prenotato al corso "+ corso.nome_corso )
    new_notifica.save()
    return redirect('/corso')

# view per la prenotazione ad un corso
@login_required(login_url='/login/')
def prenotazione_corso(request, id):
    corso = Corso.objects.get(pk=id)

    #se l'utente ha già effettuato la prenotazione
    if request.user in corso.utenti_prenotati.all() or request.user in corso.lista_attesa.all():
        return render(request, 'template_user/message.html', {'messaggio': "Hai già effettuato la prenotazione a questo corso"})

    # se la sala non ha ancora raggiunto la capienza massima
    if corso.num_utenti_prenotati < corso.sala.capienza:
        corso.num_utenti_prenotati += 1
        corso.utenti_prenotati.add(request.user)
        corso.save()
        return render(request, 'template_user/message.html', {'messaggio': "Prenotazione andata a buon fine!"})
    # se la sala ha raggiunto il numero massimo di prenotazioni aggiungo i prossimi utenti in lista d'attesa
    elif corso.num_utenti_prenotati >= corso.sala.capienza:
        # aggiugi l'utente alla coda utenti
        corso.lista_attesa.add(request.user)
        corso.save()
        return render(request,'template_user/message.html',{ 'messaggio': "Sarai aggiunto alla lista d'attesa. Verrai notificato in caso si liberi un posto."})


# view per la cancellazione della prenotazione ad un corso
@login_required(login_url='/login/')
def cancella_prenotazione(request, id):
    corso = Corso.objects.get(pk=id)

    # se l'utente che vuole cancellarsi dal corso è in lista d'attesa lo elimino da lì
    if request.user in corso.lista_attesa.all():
        corso.lista_attesa.remove(request.user)
        corso.save()
        return render(request, 'template_user/message.html', {'messaggio': "Sei stato cancellato dalla lista di attesa"})

    # se l'utente è prenotato al corso selezionato
    if request.user in corso.utenti_prenotati.all():
        # se c'è ancora spazio nella sala e non ci sono utenti in lista d'attesa
        # allora decremento di 1 il numero di utenti prenotati al corso
        # poi cancello l'utente dagli utenti prenotati
        if corso.num_utenti_prenotati < corso.sala.capienza:
            print("nel primo if"+str(corso.num_utenti_prenotati))
            corso.num_utenti_prenotati -= 1
            corso.utenti_prenotati.remove(request.user)
            corso.save()
        # quando si libera il corso invio una notifica al primo utente in lista
        # poi aggiungo alla lista degli utenti prenotati al corso il primo utente in lista di attesa
        # cancellando in fine il primo utente in lista di attesa che ormai è passato negli utenti prenotati
        elif len(corso.lista_attesa.all()) != 0:
            notifica_utente(corso.lista_attesa.first(), corso)
            corso.utenti_prenotati.add(corso.lista_attesa.first())
            corso.lista_attesa.remove(corso.lista_attesa.first())
            corso.utenti_prenotati.remove(request.user)
            corso.save()

        # se non ci sono utenti in lista d'attesa
        # decremento semplicemente il numero di utenti prenotati
        else:
            corso.num_utenti_prenotati -= 1
            corso.utenti_prenotati.remove(request.user)
            corso.save()

        corso.save()
    # se l'utente non è prenotato al corso selezionato
    else:
        return render(request, 'template_user/message.html', {'messaggio': "Non puoi cancellarti da un corso a cui non sei prenotato!"})

    return render(request, 'template_user/message.html', {'messaggio': "Prenotazione cancellata con successo!"})

# controllo se il corso inserito o modificato si sovrappone ad altri corsi
# False se si sovrappone, True altrimenti
def corso_isUnique(request, form):
    nuovo_corso_giorno = form.cleaned_data.get('giorno')

    if Corso.objects.filter(giorno=nuovo_corso_giorno).exists():
        return False
    else:
        return True

#creazione di un corso da parte di un istruttore (permission required)
@permission_required('corso.add_corso', login_url='/')
def aggiungi_corso(request):
    if request.method == 'POST':
        form = FormCreazioneCorso(request.POST, request.FILES)

        if form.is_valid():
            if corso_isUnique(request, form):
                nuovo_nome_corso = form.cleaned_data.get('nome_corso')
                nuova_immagine_corso = form.cleaned_data.get('immagine_corso')
                nuovo_giorno_corso = form.cleaned_data.get('giorno')
                nuova_sala_corso = form.cleaned_data.get('sala')

                new_corso = Corso(nome_corso=nuovo_nome_corso, immagine_corso=nuova_immagine_corso, giorno=nuovo_giorno_corso, sala=nuova_sala_corso)
                new_corso.save()
                new_corso.utenti_prenotati.add(request.user)

                return render(request, 'template_user/message.html', {'messaggio': "Corso aggiunto!"})
            else:
                return render(request, 'template_user/message.html', {'messaggio': "Il corso si sovrappone ad un altro corso!"})
        else:
            return redirect('corso:aggiungi_corso')
    else:
        form = FormCreazioneCorso()
        return render(request, 'template_corso/aggiungi_corso.html', {'form': form})


@permission_required('corso.change_corso', login_url='/')
def modifica_corso(request, id):

    if request.method == 'POST':
        corso = Corso.objects.get(pk=id)
        form = FormCreazioneCorso(request.POST, request.FILES, instance=corso)

        if form.is_valid():
            if corso_isUnique(request, form):
                nuovo_nome_corso = form.cleaned_data.get('nome_corso')
                nuova_immagine_corso = form.cleaned_data.get('immagine_corso')
                nuovo_giorno_corso = form.cleaned_data.get('giorno')
                nuova_sala_corso = form.cleaned_data.get('sala')

                new_corso = Corso(pk=id, nome_corso=nuovo_nome_corso, immagine_corso=nuova_immagine_corso, giorno=nuovo_giorno_corso, sala=nuova_sala_corso)
                new_corso.save(force_update=True)

                return render(request, 'template_user/message.html', {'messaggio': "Corso modificato!"})
            else:
                return render(request, 'template_user/message.html', {'messaggio': "Il corso modificato si sovrappone ad un altro corso!"})
        else:
            return render(request, 'template_user/message.html', {'messaggio': "La form non è valida!"})
    else:
        corso = Corso.objects.get(pk=id)
        form = FormCreazioneCorso(instance=corso)
        return render(request, 'template_corso/aggiungi_corso.html', {'form': form})

@permission_required('corso.delete_corso', login_url='/')
def cancella_corso(request, id):
    corso = Corso.objects.get(pk=id)

    corso.delete()
    return render(request, 'template_user/message.html', {'messaggio': "Corso cancellato!"})



