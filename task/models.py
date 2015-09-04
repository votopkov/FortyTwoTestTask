# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save, pre_delete
from functions import disable_for_loaddata


class Profile(models.Model):
    url_height = models.PositiveIntegerField(editable=False, default=200)
    url_width = models.PositiveIntegerField(editable=False, default=200)
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=250, default="Eneter your name")
    last_name = models.CharField(max_length=250,
                                 default="Eneter your last name")
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='images/',
                              height_field='url_height',
                              width_field='url_width',
                              blank=True, null=True)
    bio = models.TextField(blank=True, null=True, default=" ")
    email = models.EmailField(blank=True, null=True)
    jabber = models.CharField(max_length=250, blank=True, null=True)
    skype = models.CharField(max_length=250, blank=True, null=True)
    other_contacts = models.TextField(blank=True, null=True, default=" ")

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __unicode__(self):
        return self.last_name


class Requests(models.Model):
    title = models.CharField(max_length=250, default='Http_request')
    request = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title


class SavedSignals(models.Model):
    title = models.CharField(max_length=250)
    status = models.CharField(max_length=250)

    def __unicode__(self):
        return self.title + " - " + str(self.id)


@receiver(pre_save, sender=Profile)
@disable_for_loaddata
def save_profile(instance, **kwargs):
    if instance.id == None:
        save_signals = SavedSignals(title=instance.__class__.__name__, status='Created')
        save_signals.save()
    else:
        profile_obj = Profile.objects.get(id=instance.id)
        for field in profile_obj._meta.get_all_field_names():
            profile_field = getattr(profile_obj, field)
            instance_field = getattr(instance, field)
            if profile_field != instance_field:
                save_signals = SavedSignals(title=instance.__class__.__name__, status='Updated')
                save_signals.save()
                break

        else:
            save_signals = SavedSignals(title=instance.__class__.__name__, status='Saved')
            save_signals.save()



@receiver(pre_delete, sender=Profile)
def delete_profile(instance, **kwargs):
    save_signals = SavedSignals(title=instance.__class__.__name__, status='Deleted')
    save_signals.save()