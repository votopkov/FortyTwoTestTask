# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from models import Profile
from models import Requests, Task
from forms import ProfileForm, TaskForm
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
import json
from django.template.context import RequestContext


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


@login_required()
def tasks(request, template='task/task_list.html',
          page_template='task/entry_tasks.html',
          extra_context=None):
    form = TaskForm(initial={'user': request.user.id})
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Task has been created!')
    task = Task.objects.all()
    context = {
        'task': task,
        'form': form,
        'page_template': page_template
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context,context_instance=RequestContext(request))


@require_POST
@login_required()
def edit_task(request):
    task = Task.objects.get(id=request.POST.get('id'))
    copy = request.POST.copy()
    copy['user'] = request.user.id
    form = TaskForm(copy, instance=task)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Task has been updated!')
        return HttpResponseRedirect(reverse('task:tasks'))
    else:
        raise Http404


@login_required()
def update_priority(request):
    task_position_id = map(int, request.GET.getlist('positions[]'))
    for index, item in enumerate(task_position_id, start=1):
        task = Task.objects.get(id=item)
        task.priority = index
        task.save()
    return HttpResponse(status=200)