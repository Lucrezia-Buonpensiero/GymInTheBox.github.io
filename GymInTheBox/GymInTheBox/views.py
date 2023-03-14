from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request,"template_home/home_page.html")