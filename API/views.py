from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.shortcuts import render
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
