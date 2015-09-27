# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from models import Profile, Requests
from http_request import SaveHttpRequestMiddleware

client = Client()


class ProfileMethodTests(TestCase):

    def setUp(self):
        Profile.objects.create(name=u"Владимир", last_name=u"Отопков",
                               contacts=u"+380937080855")
        Profile.objects.create(name=u"Василий", last_name=u"Петров",
                               contacts=u"+380937080855")

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
        self.profile = Profile.objects.first()
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


class SaveHttpRequestTests(TestCase):

    def setUp(self):
        Requests.objects.create(request='request_1')
        Requests.objects.create(request='request_2')

    def test_request_list(self):
        """
        Testing request list view function
        """
        # get request_list
        response = client.get(reverse('task:request_list'))
        # test entering the page
        self.assertEquals(response.status_code, 200)

    def test_request_list_ajax(self):
        """
        Testing request list view function
        """
        # get requests
        response = client.get(reverse('task:request_list_ajax'),
                              content_type='application/json',
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # get first request
        request = Requests.objects.get(request='request_1')
        # get second request
        request_2 = Requests.objects.get(request='request_2')
        # get nonexistent request
        request_3 = Requests.objects.filter(request='request_3')
        # test getting request list
        self.assertEquals(response.status_code, 200)
        # test first request in response content
        self.assertContains(response, request)
        # test second request in response content
        self.assertContains(response, request_2)
        # test not exist request in response content
        self.assertNotIn(response.content, request_3)

    def test_request_detail(self):
        """
        Testing request detail view function
        """
        # get first request
        request = Requests.objects.get(request='request_1')
        # get first request
        response = client.get(reverse('task:request_detail',
                                      args=(request.id, )))
        # get nonexistent request
        response_2 = client.get(reverse('task:request_detail',
                                        args=(555, )))
        # test gettings page with first profile
        self.assertEqual(response.status_code, 200)
        # test gettings page with nonexistent request
        self.assertEqual(response_2.status_code, 404)
        # test first request data on the page
        self.assertIn(request.request, response.content)
        # test context of the detail request
        self.assertEqual(request, response.context['obj'])

    def test_save_request(self):
        # create client and savehttpr... instance
        self.save_http = SaveHttpRequestMiddleware()
        self.new_request = Client()
        """
        Test SaveHttpRequestMiddleware()
        """
        # save request to DB
        self.save_http.process_request(request=self.new_request)
        # test saving request to DB
        self.assertEqual(Requests.objects.all().count(), 3)


class SaveRequestAdditionalTest(TestCase):
    fixtures = ['initial_data.json']

    def test_last_requests(self):
        """
        Testing the requests in the right order
        """
        # test count of requests in db
        self.assertEqual(Requests.objects.all().count(), 15)
        # test if new request is the first
        self.assertEqual(Requests.objects.first().id, 15)
