# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from PIL import Image, ImageOps
from django.dispatch.dispatcher import receiver


class Profile(models.Model):
    url_height = models.PositiveIntegerField(editable=False, default=200)
    url_width = models.PositiveIntegerField(editable=False, default=200)
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=250, default="Eneter your name")
    last_name = models.CharField(max_length=250,
                                 default="Eneter your last name")
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='images/',
                              blank=True,
                              null=True)
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


@receiver(post_save, sender=Profile)
def post_save(instance, **kwargs):
    if instance.photo:
        image = Image.open(instance.photo)
        imagefit = ImageOps.fit(image, (200, 200), Image.ANTIALIAS)
        photo_path = instance.photo.url.replace("/", "", 1)
        imagefit.save(photo_path, 'JPEG', quality=75)


class Requests(models.Model):
    title = models.CharField(max_length=250, default='Http_request')
    request = models.TextField()
    path = models.CharField(max_length=250, blank=True, null=True)
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
