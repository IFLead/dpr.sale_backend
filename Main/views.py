from django.shortcuts import render, redirect

from Main.models import Category, Post


def index(request):
    return render(request, 'index.html', {'categories':Category.objects.all(), 'posts':Post.objects.all()})


def post_view(request, post_id):
    return render(request, 'ad.html', {'post':Post.objects.get(pk=post_id)})


def sign_up(request):
    return render(request, 'sign_up.html')