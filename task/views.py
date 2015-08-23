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

