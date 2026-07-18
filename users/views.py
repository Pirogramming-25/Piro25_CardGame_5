from django.shortcuts import render


def home(request):
    return render(request, "users/home.html")


def login(request):
    return render(request, "users/login.html")
