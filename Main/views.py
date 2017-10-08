from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from filer.fields.image import FilerImageField

from Main.models import Category, Post, City, Image
from django.core.files import File
from filer.models import Image as FImage

from Realtor import settings


def index(request):
    return render(request, 'index.html',
                  {'categories': Category.objects.all(),
                   'posts': Post.objects.filter(is_top=True, verified=True, closed=False).order_by('?')[:8],
                   'cities': City.objects.all(), 'self_posts': Post.objects.filter(owner_id__exact=request.user.id),
                   'user': request.user})


@staff_member_required
def dashboard(request):
    return render(request, 'dashboard.html',
                  {'posts_not_verified': Post.objects.filter(verified=False, closed=False),
                   'posts_closed': Post.objects.filter(closed=True),
                   'accounts': User.objects.filter(custom__verified=False),
                   'self_posts': Post.objects.filter(owner_id__exact=request.user.id)})


def post_view(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        user_is_owner = post.owner.id == request.user.id
        if post.verified or user_is_owner or request.user.is_staff:
            return render(request, 'post.html',
                          {'post': post, 'self_posts': Post.objects.filter(owner_id__exact=request.user.id),
                           'user_is_owner': user_is_owner, 'user_is_staff': request.user.is_staff, })
            # 'user_is_verified': request.user.custom.is_verified
        else:
            return HttpResponseForbidden()
    except Post.DoesNotExist:
        return HttpResponseNotFound()


def new_post(request):
    if request.method == 'POST' and request.user.custom.verified:

        post = Post()
        post.category_id = int(request.POST["post_type"][0])

        # my_file = File(open(filenames[0]))
        post.main_photo = FImage.objects.create(file=request.FILES['main_photo'],
                                                original_filename=request.FILES['main_photo'].name, owner=request.user)

        post.title = request.POST["title"]
        post.description = request.POST["description"]
        post.price = int(request.POST["estate_price"])
        post.currency = int(request.POST["estate_currency"])
        post.owner_id = request.user.id

        post.rooms = int(request.POST["rooms_count"])
        post.floor = int(request.POST["estate_floor"])
        post.storeys = int(request.POST["estate_storeys"])
        post.district_id = int(request.POST["estate_district"])
        post.save()
        for i in range(1, 8):
            if 'hidden-new-file' + str(i) in request.FILES:
                fimg = FImage.objects.create(file=request.FILES['hidden-new-file' + str(i)],
                                             original_filename=request.FILES['hidden-new-file' + str(i)].name,
                                             owner=request.user)

                img = Image()
                img.image_file=fimg
                img.obj_id=post.id
    return redirect('/')


def sign_up(request):
    return render(request, 'sign_up.html')
