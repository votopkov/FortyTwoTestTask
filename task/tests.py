# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase, RequestFactory
from models import Profile, Requests
from middleware import SaveHttpRequestMiddleware
import json
from django.utils.encoding import smart_unicode

client = Client()


class ProfileMethodTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
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

    def test_unicode(self):
        """
        Test unicode data on the page
        """
        profile = Profile.objects.first()
        self.assertEqual(smart_unicode(profile), u'Отопков')

    def test_db_entries_count(self):
        """
        Test db entries
        """
        profile = Profile.objects.all().count()
        # one profile in fixtures and one in setUp
        self.assertEqual(profile, 2)

    def test_admin(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_admin_login(self):
        admin = {'name': 'admin',
                 'password': 'admin'}
        response = self.client.post(reverse('admin:index'), admin)
        self.assertEqual(response.status_code, 200)

    def test_index_html(self):
        response = self.client.get(reverse('task:index'))
        self.assertTrue('<h1>42 Coffee Cups Test Assignment</h1>'
                        in response.content)


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

    def test_db_entries_count(self):
        """
        Test db entries
        """
        profile = Profile.objects.all().count()
        self.assertEqual(profile, 0)


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
        # create new 10 requests will be 12 requests in db
        i = 0
        while i < 10:
            Requests.objects.create(request='test_request')
            i += 1
        # get requests
        response = client.get(reverse('task:request_list_ajax'),
                              content_type='application/json',
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # get first request
        request = Requests.objects.get(request='request_1')
        # get second request
        request_2 = Requests.objects.get(request='request_2')
        # test getting request list
        self.assertEquals(response.status_code, 200)
        # test first request in response content
        self.assertContains(response, request)
        # test second request in response content
        self.assertContains(response, request_2)
        # get json response and loads it
        response_list = json.loads(response.content)
        # test if 10 requests in response
        resp_list_count = sum(1 for x in response_list)
        self.assertEqual(resp_list_count, 10)

    def test_last_requests(self):
        """
        Testing the requests in the right order
        """
        # test count of requests in db
        self.assertEqual(Requests.objects.all().count(), 2)
        # test if new request is the first
        self.assertEqual(Requests.objects.first().id, 2)

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
        """
        Test SaveHttpRequestMiddleware()
        """
        # create client and savehttpr... instance
        self.save_http = SaveHttpRequestMiddleware()
        self.new_request = RequestFactory().get(reverse('task:index'))
        # save request to DB
        self.save_http.process_request(request=self.new_request)
        # test saving request to DB
        self.assertEqual(Requests.objects.all().count(), 3)


class SaveHttpRequestNoDataTests(TestCase):

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
        self.assertEquals(response.status_code, 200)

    def test_request_detail(self):
        """
        Testing request detail view function
        """
        # get request
        response = client.get(reverse('task:request_detail',
                                      args=(2, )))
        # test gettings page with unexisted request
        self.assertEqual(response.status_code, 404)
