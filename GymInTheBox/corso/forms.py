from django.forms import ModelForm
from corso.models import Corso

class FormCreazioneCorso(ModelForm):
    class Meta:
        model = Corso
        fields = ['nome_corso', 'immagine_corso', 'giorno', 'sala']