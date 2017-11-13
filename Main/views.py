from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect
from filer.models import Image as FImage

from Main.models import Category, Post, City, Image, District


def index(request):
    return render(request, 'index.html',
                  {'categories': Category.objects.all(),
                   'posts': Post.objects.filter(is_top=True, verified=True, closed=False).order_by('?')[:12],
                   'cities': City.objects.all(),  # 'self_posts': Post.objects.filter(owner_id__exact=request.user.id),
                   'user': request.user})


@staff_member_required
def dashboard(request):
    return render(request, 'dashboard.html',
                  {'posts_not_verified': Post.objects.filter(verified=False, closed=False),
                   'posts_closed': Post.objects.filter(closed=True),
                   'accounts': User.objects.filter(custom__verified=False),
                   'self_posts': Post.objects.filter(owner_id__exact=request.user.id)})


@login_required
def my(request):
    return render(request, 'my.html',
                  {'posts': Post.objects.filter(owner_id__exact=request.user.id)})


def post_view(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        user_is_owner = post.owner.id == request.user.id
        if post.verified or user_is_owner or request.user.is_staff:
            return render(request, 'post.html',
                          {'post': post, 'self_posts': Post.objects.filter(owner_id__exact=request.user.id),
                           'cities': City.objects.all(), 'categories': Category.objects.all(),
                           'districts': District.objects.all(),
                           'user_is_owner': user_is_owner, 'user_is_staff': request.user.is_staff, })
            # 'user_is_verified': request.user.custom.is_verified
        else:
            return HttpResponseForbidden()
    except Post.DoesNotExist:
        return HttpResponseNotFound()


def str2bool(v):
    return v.lower() in 'true'


def new_post(request):
    if request.method == 'POST' and request.user.custom.verified:

        post = Post()
        post.category_id = int(request.POST["post_type"])

        # my_file = File(open(filenames[0]))
        if 'main_photo' in request.FILES:
            post.main_photo = FImage.objects.create(file=request.FILES['main_photo'],
                                                    original_filename=request.FILES['main_photo'].name,
                                                    owner=request.user)

        post.title = request.POST["title"]
        post.description = request.POST["description"]
        post.price = int(request.POST["estate_price"])
        post.currency = int(request.POST["estate_currency"])
        post.owner_id = request.user.id

        post.rooms = int(request.POST["rooms_count"])
        post.square = float(request.POST["estate_square"])
        post.floor = int(request.POST["estate_floor"])
        post.storeys = int(request.POST["estate_storeys"])
        post.city_id = int(request.POST["estate_city"])
        post.district_id = int(request.POST["estate_district"])
        post.is_important = str2bool(request.POST["is_important"])
        if request.user.is_staff:
            post.verified = True
        post.save()
        files = request.FILES.getlist('hidden-new-file')
        for file in files:
            fimg = FImage.objects.create(file=file,
                                         original_filename=file.name,
                                         owner=request.user)

            img = Image()
            img.image_file = fimg
            img.obj_id = post.id
            img.save()
    return redirect('/')


def sign_up(request):
    return render(request, 'sign_up.html')
