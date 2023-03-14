from django.contrib import admin
from .models import Corso
from .models import Giorno
from .models import Sala
# Register your models here.
admin.site.register(Corso)
admin.site.register(Giorno)
admin.site.register(Sala)