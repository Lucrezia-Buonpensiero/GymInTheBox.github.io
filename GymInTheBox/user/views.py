from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail
from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist
from user.models import Tessera
from .models import *
from .forms import FormRegistrazione
from .forms import *
from django.contrib.auth.models import User


# Create your views here.

def numero_tessera_isUnique(form):
    tessera = str(form.cleaned_data.get('numero_tessera'))

    for t in Tessera.objects.all():
        if str(t.numero_tessera) == tessera:
            return False
    else:
        return True


def email_isUnique(request, form):
    email = str(form.cleaned_data.get('email'))

    if User.objects.filter(email=email).exists():
        return False
    else:
        return True

# Metodo per la gestione della registrazione
def Registration(request):
    if request.method == 'POST':
        form = FormRegistrazione(request.POST)

        if form.is_valid():
            # controllo se il numero tessera inserito da input esiste già
            if numero_tessera_isUnique(form):
                if email_isUnique(request, form):
                    form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    numero_tessera = form.cleaned_data.get('numero_tessera')
                    user = authenticate(username=username, password=raw_password)

                    new_tessera = Tessera(numero_tessera=numero_tessera, user_id=user.id)
                    new_tessera.save()

                    login(request, user)
                    return redirect('user:area_utente')
                else:
                    return render(request, 'template_user/message.html', {'messaggio': "Ti stai registrando con una mail già presente"})
            else:
                return render(request, 'template_user/message.html', {'messaggio': "Il numero tessera esiste già"})
        else:
            return render(request, 'template_user/registrati.html', {'form': form})
    else:
        form = FormRegistrazione()
        return render(request, 'template_user/registrati.html', {'form': form})

# Area Utente
@login_required(login_url='/login/')
def area_utente(request):
    if request.user is not None:
        if request.user.is_active:
            login(request, request.user)
            try:
                utente = Tessera.objects.get(user=request.user)
                lista_notifiche = Notifica.objects.filter(user=request.user)


                numero_tessera = utente.numero_tessera
                context = {'lista_notifiche': lista_notifiche, 'numero_tessera': numero_tessera}
            except Tessera.DoesNotExist:
                return render(request, 'template_user/message.html', {'messaggio': "L'utente non ha una tessera!"})

            if request.user.is_staff:
                return render(request, 'template_user/area_istruttore.html', context)
            else:
                return render(request, 'template_user/area_utente.html', context)
        else:
            return HttpResponse("Non riusciamo a trovare il tuo profilo...Prova a registrarti!")

@login_required(login_url='/login/')
def cancella_notifiche(request):
    Notifica.objects.filter(user=request.user).delete()
    return render(request, 'template_user/message.html', {'messaggio': "Lista notifiche cancellata!"})


#Metodo per la gestione del logout
@login_required(login_url='/login/')
def Logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def contact(request):
    if request.method == 'POST': #if the form has been submitted
        form = ContactForm(request.POST) #istanza bound (con dati) Recupero i dati già divisi nei campi appositi
        if form.is_valid(): #step di validazione dei dati
            #dictionary form.cleaned_data
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email_dest = form.cleaned_data['email_dest']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = [] #destinatari della mail

            if cc_myself:
                recipients.append(email_dest) #aggiungo il sender tra i destinatari

            send_mail(subject, message, email_dest, recipients) #spedizione della email richiede configurazione smtp in settings.py
            return render(request, 'template_user/message.html',{'messaggio': "Email inviata!"})

        else:
            return render(request, 'template_user/message.html',{'messaggio': "OPS, qualcosa è andato storto!"})
    else: #GET request: just visualize the form
        form = ContactForm() #An unbound form : non ha dati associati da db -campi vuoti o con i default
        return render(request, 'template_user/contact.html', {'form': form}) # form:form passo la form unbound al template contact.html

