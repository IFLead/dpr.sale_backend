from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from Main.models import Category, Post, City


def index(request):
    return render(request, 'index.html',
                  {'categories': Category.objects.all(), 'posts': Post.objects.filter(is_top=True, verified=True),
                   'cities': City.objects.all()})


@staff_member_required
def dashboard(request):
    return render(request, 'dashboard.html',
                  {'posts': Post.objects.filter(verified=False), 'cities': City.objects.all()})


def post_view(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        user_is_owner = post.owner.id == request.user.id
        if post.verified or user_is_owner:
            return render(request, 'post.html', {'post': post, 'user_is_owner': user_is_owner})
        else:
            return HttpResponseForbidden()
    except Post.DoesNotExist:
        return HttpResponseNotFound()


def sign_up(request):
    return render(request, 'sign_up.html')
