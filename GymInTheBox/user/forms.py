from django.forms import ModelForm
from django import forms
from .models import Tessera
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#class FormProfiloUtente(forms.ModelForm):
#    class Meta:
#        model = Tessera
       # fields = ('notifica', )

class FormRegistrazione(UserCreationForm) :
    email = forms.EmailField(max_length=150)
    numero_tessera = forms.CharField(max_length=4, help_text="Deve registrarti un istruttore per ricevere un numero tessera valido")
    #first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'numero_tessera', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    email_dest = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
