
# GymInTheBox

WebApp sviluppata con framework Django, per la gestione di un sito di una palestra.




## AUTHOR: BUONPENSIERO LUCREZIA
> MATRICOLA: 110796


## DB Utilizzato: SQLITE3

### CREAZIONE DB
```console
 python3 manage.py makemigrations
```
```console
 python3 manage.py migrate
```

### CREAZIONE SUPERUSER
```console
 $ python3 manage.py createsuperuser
 ```

### AVVIO PROGETTO
```console
 python3 manage.py runserver
 ```

### AVVIO TEST SULLE VIEW

#### RUN ALL:
```console
 python3 manage.py test
 ```

#### RUN USER TEST APP:
```console
python3 manage.py test user
 ```

### AVVIO SERVER SMTP
```console
python3 -m smtpd -n -c DebuggingServer localhost:1025
```
