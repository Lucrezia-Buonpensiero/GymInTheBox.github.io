from django.db import models
from django.contrib.auth.models import User

class Notifica(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notifica = models.TextField()

# Create your models here.
class Tessera(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_tessera = models.PositiveIntegerField(primary_key=True)
    #tipo_abbonamento = models.CharField(max_length=20)
    #data_inizio_abbonamento = models.DateField()
    #data_fine_abbonamento = models.DateField()
    notifiche = models.ForeignKey(Notifica, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.numero_tessera)

