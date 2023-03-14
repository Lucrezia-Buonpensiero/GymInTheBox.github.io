from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from .views import numero_tessera_isUnique
from .forms import FormRegistrazione

from user.models import Tessera
# Create your tests here.

class TestLoginModel(TestCase):

    def test_login_ok(self):
        """
        Test che simula il login corretto, ovvero con utente presente nel db
        """
        user = User.objects.create(username='usertest')
        user.set_password('testpassword1')
        user.save()
        client = Client()
        login_ok = client.login(username='usertest', password='testpassword1')
        self.assertTrue(login_ok)

    def test_login_bad(self):
        """
        Test che simula il login con utente NON presente nel database
        """
        client = Client()
        bad_login = client.login(username='baduser', password='badpassword1')
        self.assertFalse(bad_login)

    def test_numero_tessera_isUnique(self):
        """
        Test che verifica la correttezza del metodo numero_tessera_isUnique
        Il metodo ritorna False se trova una tessera con lo stesso numero, True altrimenti
        """
        tessera = Tessera.objects.create(numero_tessera='1234', user_id='1')
        tessera.save()
        form_data = {'username': 'username',
                     'numero_tessera': '1234',
                     'first_name': 'firstname',
                     'last_name': 'lastname',
                     'email': 'email@email.it',
                     'password1': 'dummypassword',
                     'password2': 'dummypassword'}

        form = FormRegistrazione(data=form_data)
        form.save()

        self.assertFalse(numero_tessera_isUnique(form))

    def test_numero_tessera_is_NOT_Unique(self):
        """
        Test che verifica la correttezza del metodo sopra citato,
        con numeri tessere diversi. Quindi ritornerà True
        """
        tessera = Tessera.objects.create(numero_tessera='9999', user_id='1')
        tessera.save()
        form_data = {'username': 'username',
                     'numero_tessera': '1234',
                     'first_name': 'firstname',
                     'last_name': 'lastname',
                     'email': 'email@email.it',
                     'password1': 'dummypassword',
                     'password2': 'dummypassword'}

        form = FormRegistrazione(data=form_data)
        form.save()

        self.assertTrue(numero_tessera_isUnique(form))