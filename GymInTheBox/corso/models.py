from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# Create your models here.

class Sala(models.Model):
    SALA1 = 1
    SALA2 = 2
    SALA3 = 3
    SALA4 = 4
    SALA5 = 5

    SALE = [
        (SALA1, 'sala 1'),
        (SALA2, 'sala 2'),
        (SALA3, 'sala 3'),
        (SALA4, 'sala 4'),
        (SALA5, 'sala 5'),
    ]

    numero_sala = models.IntegerField(choices=SALE, default='sala 1')
    #da fare il controllo nelle view per max value min value
    capienza = models.PositiveIntegerField(default=5)

    def __str__(self):
        return str(self.numero_sala)


class Giorno(models.Model):
    LUNEDI = 'Lunedì'
    MARTEDI = 'Martedì'
    MERCOLEDI = 'Mercoledì'
    GIOVEDI = 'Giovedì'
    VENERDI = 'Venerdì'
    SABATO = 'Sabato'

    GIORNI = [
        (LUNEDI, 'Lunedì'),
        (MARTEDI, 'Martedì'),
        (MERCOLEDI, 'Mercoledì'),
        (GIOVEDI, 'Giovedì'),
        (VENERDI, 'Venerdì'),
        (SABATO, 'Sabato')
    ]
    nome_giorno = models.CharField(max_length=15,choices=GIORNI,default='Lunedì')
    ora_corso = models.TimeField(default='00:00')

    def __str__(self):
        nome_giorno = str(self.nome_giorno)
        ora_corso = str(self.ora_corso)
        return str(nome_giorno+" "+ora_corso)

class Corso(models.Model):
    nome_corso = models.CharField(max_length=30, default="VUOTO")
    immagine_corso = models.ImageField(upload_to='', default='missing.jpg')
    giorno = models.ForeignKey(Giorno, on_delete=models.CASCADE, default='')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, default='')
    num_utenti_prenotati = models.PositiveIntegerField(default=1)
    utenti_prenotati = models.ManyToManyField(User, related_name="utenti_prenotati")
    lista_attesa = models.ManyToManyField(User, related_name="lista_attesa", blank=True)

    def __str__(self):
        return str(self.nome_corso)


