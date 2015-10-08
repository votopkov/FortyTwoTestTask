# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from models import Profile
client = Client()


class ProfileMethodTests(TestCase):

    def setUp(self):
        Profile.objects.create(name=u"Владимир", last_name=u"Отопков")
        Profile.objects.create(name=u"Василий", last_name=u"Петров")
        # get main page
        self.response = self.client.get(reverse('task:index'))

    def test_enter_main_page(self):
        """
        Test entering main page
        """
        # if index page exists
        self.assertEqual(self.response.status_code, 200)

    def test_profile(self):
        """
        Testing profile shown in the page
        """
        # get profile
        profile = Profile.objects.first()
        self.assertEqual(self.response.context['profile'], profile)
        # test profile data exist on the main page
        self.assertContains(self.response, u'Отопков')
        self.assertContains(self.response, u'Владимир')

    def test_non_another_profile(self):
        """
        Test if exist another profile in the page
        """
        # test if not another profile on index
        self.assertNotEqual(self.response.context['profile'],
                            Profile.objects.get(id=2))
        self.assertNotIn('Василий', self.response.content)


class ProfileNoDataMethodTests(TestCase):

    def setUp(self):
        # get main page
        self.response = self.client.get(reverse('task:index'))

    def test_enter_main_page(self):
        """
        Test entering main page
        """
        # if index page exists
        self.assertEqual(self.response.status_code, 200)

    def test_profile(self):
        """
        Testing profile shown in the page
        """
        # get profile
        profile = Profile.objects.all().count()
        self.assertEqual(profile, 0)
        # test profile data exist on the main page
        self.assertNotContains(self.response, u'Отопков')
        self.assertNotContains(self.response, u'Владимир')
