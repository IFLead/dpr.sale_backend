from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.loader import render_to_string

from Main.models import District, Post
from django.http import JsonResponse


def districts(request):
    return JsonResponse(list(District.objects.filter(city_id__exact=request.GET['city_id']).values('id', 'name')),
                        safe=False)


@staff_member_required
def top_post(request):
    try:
        post = Post.objects.get(pk=request.POST['post_id'])
        post.is_top = True
        post.save()
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'has no this object'})
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def untop_post(request):
    try:
        post = Post.objects.get(pk=request.POST['post_id'])
        post.is_top = False
        post.save()
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'has no this object'})
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def verify_post(request):
    try:
        post = Post.objects.get(pk=request.POST['post_id'])
        post.verified = True
        post.save()
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'has no this object'})
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def unverify_post(request):
    try:
        post = Post.objects.get(pk=request.POST['post_id'])
        post.verified = False
        post.save()
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'has no this object'})
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'unknown error'})


@login_required
def delete_post(request):
    try:
        post = Post.objects.get(pk=request.POST['post_id'])
        if request.user.is_active and (request.user.is_staff or post.owner.id == request.user.id):
            post.delete()
        else:
            return JsonResponse({'status': 'error', 'message': 'you have not access'})
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'has no this object'})
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def verify_user(request):
    try:
        post = User.objects.get(pk=request.POST['user_id'])
        post.verified = True
        post.save()
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'has no this object'})
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def unverify_user(request):
    try:
        post = User.objects.get(pk=request.POST['user_id'])
        post.verified = False
        post.save()
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'has no this object'})
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'unknown error'})


def rename_dict_keys(d, names: dict):
    for k, v in names.items():
        if k in d:
            d[v] = d.pop(k)


def search(request):
    names = {'city': 'district__city', 'min_square': 'square__gte', 'max_square': 'square__lte',
             'min_walls': 'rooms__gte', 'max_walls': 'rooms__lte', 'min_floor': 'floor__gte', 'max_floor': 'floor__lte',
             'min_price': 'price__gte', 'max_price': 'price__lte', }
    # category: -1
    # city: 1 district__city
    # district: -1
    # min_square: square__gte
    # max_square: square__lte
    # min_walls: rooms__gte
    # max_walls: rooms__lte
    # min_floor: floor__gte
    # max_floor: floor__lte
    # min_price: price__gte
    # max_price: price__lte
    # currency: 0
    filters = {k: v for k, v in request.POST.items() if v and v != '-1'}
    if 'min_price' not in filters and 'max_price' not in filters:
        filters.pop('currency')
    else:
        if filters['currency'] == 1:
            if 'min_price' not in filters:
                filters['min_price'] *= 60
            if 'max_price' not in filters:
                filters['max_price'] *= 60
        filters.pop('currency')
    rename_dict_keys(filters, names)
    posts = Post.objects.filter(is_top=True,**filters)
    return JsonResponse({'status': 'OK', 'html': render_to_string('ajax-posts.html', {'posts': posts})})
