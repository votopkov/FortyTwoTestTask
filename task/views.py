# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf import settings
from models import Profile


def main(request):
    profile = Profile.objects.get(id=settings.DEFAULT_PROFILE_ID)
    context = dict(profile=profile)
    return render(request, 'task/main.html', context)
