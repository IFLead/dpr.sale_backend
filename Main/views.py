from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html')


def ad(request):
    return render(request, 'ad.html')


def sign_up(request):
    return render(request, 'sign_up.html')