# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from models import Profile
from django.conf import settings
client = Client()


class ProfileMethodTests(TestCase):

    def setUp(self):
        Profile.objects.create(name=u"Владимир", last_name=u"Отопков",
                               contacts=u"+380937080855")
        Profile.objects.create(name=u"Василий", last_name=u"Петров")

    def test_enter_main_page(self):
        """
        Testing my profile shown on the main page
        Testing one profile if two
        Testing unicode
        """
        response = self.client.get(reverse('task:index'))
        # if index page exists
        self.assertEqual(response.status_code, 200)
        # get profile
        self.profile = Profile.objects.get(id=settings.DEFAULT_PROFILE_ID)
        self.assertEqual(response.context['profile'], self.profile)
        # test if not another profile on index
        self.assertNotEqual(response.context['profile'],
                            Profile.objects.get(id=2))
        # test profile data exist on the main page
        self.assertContains(response, u'Отопков')
        self.assertContains(response, u'Владимир')
        self.assertContains(response, '+380937080855')
        # test if not another profile on the main page
        self.assertNotIn('Василий', response.content)
