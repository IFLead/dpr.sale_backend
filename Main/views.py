from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden, HttpResponseNotFound, JsonResponse

from Main.models import Category, Post, City, Image


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
        fs = FileSystemStorage()

        main_photo = request.FILES['main_photo']
        filename = fs.save(main_photo.name, main_photo)
        # uploaded_file_url = fs.url(filename)
        filenames = [filename]
        for i in range(1, 8):
            if 'hidden-new-file' + str(i) in request.FILES:
                photo = request.FILES['hidden-new-file' + str(i)]
                filename = fs.save(photo.name, photo)
                filenames.append(filename)

        post = Post()
        post.category_id = int(request.POST["post_type"][0])
        post.main_photo = filenames.pop(0)
        post.title = request.POST["title"][0]
        post.description = request.POST["description"][0]
        post.price = int(request.POST["estate_price"][0])
        post.currency = int(request.POST["estate_currency"][0])
        post.owner_id = request.user.id

        post.rooms = int(request.POST["rooms_count"][0])
        post.floor = int(request.POST["estate_floor"][0])
        post.storeys = int(request.POST["estate_storeys"][0])
        post.district = int(request.POST["estate_district"][0])
        post.save()
        for filename in filenames:
            Image(image_file=filename, obj_id=post.id).save()
    return JsonResponse({'url': dict(request.POST)})


def sign_up(request):
    return render(request, 'sign_up.html')
