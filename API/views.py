from django.shortcuts import render
from Main.models import District
from django.http import JsonResponse


def districts(request):
    return JsonResponse(list(District.objects.filter(city_id__exact=request.GET['city_id']).values('id', 'name')), safe=False)