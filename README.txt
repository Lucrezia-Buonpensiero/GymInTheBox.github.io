------------------------------------
--- PROGETTO INTERFACCE UTENTE -----
------------------------------------
--- AUTHOR: BUONPENSIERO LUCREZIA---
--- MATRICOLA: 110796 --------------
------------------------------------


--- DB UTILIZZATO: SQLITE3 ---

--- CREAZIONE DB:
--- >$ python3 manage.py makemigrations
--- >$ python3 manage.py migrate

--- CREAZIONE SUPERUSER:
--- >$ python3 manage.py createsuperuser

--- AVVIO PROGETTO:
--- >$ python3 manage.py runserver

--- AVVIO TEST SULLE VIEW:
--- RUN ALL:
--- >$ python3 manage.py test
--- RUN USER TEST APP:
--- >$ python3 manage.py test user

--- AVVIO SERVER SMTP:
--- >$ python3 -m smtpd -n -c DebuggingServer localhost:1025
