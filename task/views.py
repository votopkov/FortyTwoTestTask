# -*- coding: utf-8 -*-
from django.core import serializers
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from models import Profile
from models import Requests


def main(request):
    profile = Profile.objects.get(id=settings.DEFAULT_PROFILE_ID)
    context = dict(profile=profile)
    return render(request, 'task/main.html', context)


def request_list(request):
    if request.is_ajax():
        data = serializers.serialize("json", Requests.objects.all()[:10])
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404


def request_detail(request, identify):
    obj = get_object_or_404(Requests, pk=identify)
    context = dict(obj=obj)
    return render(request, 'task/request_detail.html', context)
