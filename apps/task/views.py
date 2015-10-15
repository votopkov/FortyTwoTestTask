# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from models import Profile
from models import Requests
from forms import ProfileForm
from django.views.decorators.http import require_POST
import json


def main(request):
    profile = Profile.objects.first()
    user_form = ProfileForm(instance=profile)
    context = dict(profile=profile, user_form=user_form)
    return render(request, 'task/main.html', context)


@login_required()
def edit_profile(request):
    profile = Profile.objects.first()
    user_form = ProfileForm(instance=profile)
    context = dict(profile=profile, user_form=user_form)
    return render(request, 'task/edit_profile.html', context)


def request_list(request):
    return render(request, 'task/request_list.html')


def request_list_ajax(request):
    if request.is_ajax():
        data = serializers.serialize("json", Requests.objects.all()[:10])
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404


@login_required()
def request_detail(request, identify):
    obj = get_object_or_404(Requests, pk=identify)
    context = dict(obj=obj)
    return render(request, 'task/request_detail.html', context)


@login_required()
@require_POST
def update_profile(request):
    identify = request.POST.get('id')
    profile = Profile.objects.get(id=identify)
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        form.save()
        profile = Profile.objects.get(id=int(identify))
        profile_to_json = {'status': "success",
                           'image_src': profile.photo.url
                           if profile.photo else ''}
    else:
        profile_to_json = {'status': "error",
                           'image_src': profile.photo.url
                           if profile.photo else ' '}

    return HttpResponse(json.dumps(profile_to_json),
                        content_type="application/json")
