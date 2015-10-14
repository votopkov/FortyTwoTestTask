# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase, RequestFactory
from models import Profile, Requests
from middleware import SaveHttpRequestMiddleware
import json
from django.utils.encoding import smart_unicode
from forms import ProfileForm


client = Client()


class ProfileMethodTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        user = User.objects.create(username='guest', password='guest')
        Profile.objects.create(name=u"Василий", last_name=u"Петров", user=user)
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
        """
        Test admin
        """
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_admin_login(self):
        """
        Test enter admin part
        """
        admin = {'name': 'admin',
                 'password': 'admin'}
        response = self.client.post(reverse('admin:index'), admin)
        self.assertEqual(response.status_code, 200)

    def test_index_html(self):
        """
        Test valid html
        """
        response = self.client.get(reverse('task:index'))
        self.assertTrue('<h1>42 Coffee Cups Test Assignment</h1>'
                        in response.content)

    def test_entering_edit_profile(self):
        # test login required
        test_login_req_response = client.post(
            reverse('task:edit_profile')
        )
        self.assertEqual(test_login_req_response.status_code, 302)
        # login
        self.client.login(username='admin', password='admin')
        # get edit page with login user
        response = self.client.get(reverse('task:edit_profile'))
        self.assertEqual(response.status_code, 200)
        # test if form is on the page (Save - submit button)
        self.assertContains(response, 'Save')

    def test_send_post_data_update_profile(self):
        """
        Testing update profile
        """
        form_data = {
            'id': 2,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # test login required
        test_login_req_response = self.client.post(
            reverse('task:update_profile'), form_data
        )
        self.assertEqual(test_login_req_response.status_code, 302)
        # login
        self.client.login(username='admin', password='admin')
        # test method (get not allowed)
        test_method_response = self.client.get(
            reverse('task:update_profile')
        )
        self.assertEqual(test_method_response.status_code, 405)
        # update Vasiliy Petrov
        self.client.post(reverse('task:update_profile'), form_data)
        # get Vasiliy Petrov profile
        profile = Profile.objects.get(id=2)
        # test if it is updated
        self.assertEqual(profile.name, 'admin')
        self.assertEqual(profile.email, 'mail@mail.ua')

    def test_send_unvalid_post_data_update_profile(self):
        """
        Testing not update profile unvalid data
        """
        form_data = {
            'id': 2,
            'name': 'ad',  # min 3 simbols
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # test login required
        test_login_req_response = self.client.post(
            reverse('task:update_profile'), form_data
        )
        self.assertEqual(test_login_req_response.status_code, 302)
        self.client.login(username='admin', password='admin')
        # update Vasiliy Petrov
        self.client.post(reverse('task:update_profile'), form_data)
        # get Vasiliy Petrov profile
        profile = Profile.objects.get(pk=2)
        # test if name was updated
        self.assertEqual(profile.name, smart_unicode(u'Василий'))
        # test if Vasiliy has new email
        self.assertNotEqual(profile.email, 'mail@mail.ua')


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
        self.assertNotContains(self.response, '+380937080855')

    def test_main_page_not_login_in_user(self):
        """
        Testing profile update form
        """
        # get page
        response = self.client.get(reverse('task:index'))
        # if index page exists
        self.assertEqual(response.status_code, 200)
        # test form not exist
        self.assertNotContains(response, 'Save')


class SaveHttpRequestTests(TestCase):

    def setUp(self):
        Requests.objects.create(request='request_1')
        Requests.objects.create(request='request_2')
        User.objects.create_user('admin', ' ', 'admin')

    def test_request_list(self):
        """
        Testing request list view function
        """
        # get request_list
        client.login(username='admin', password='admin')
        response = client.get(reverse('task:request_list'))
        # test entering the page
        self.assertEquals(response.status_code, 200)

    def test_request_list_ajax(self):
        """
        Testing request list view function
        """
        # login user
        client.login(username='admin', password='admin')
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
        client_2 = Client()
        client.login(username='admin', password='admin')
        request = Requests.objects.get(request='request_1')
        # get first request
        response = client.get(reverse('task:request_detail',
                                      args=(request.id, )))
        # get nonexistent request
        response_2 = client.get(reverse('task:request_detail',
                                        args=(555, )))
        # get response with not login user
        response_3 = client_2.get(reverse('task:request_detail',
                                          args=(request.id, )))
        # test gettings page with first profile
        self.assertEqual(response.status_code, 200)
        # test gettings page with nonexistent request
        self.assertEqual(response_2.status_code, 404)
        # test not login user
        self.assertEqual(response_3.status_code, 302)
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
        self.new_request = RequestFactory().get('/')
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
        self.assertEqual(response.status_code, 302)
        # create user to test
        User.objects.create_user('admin', ' ', 'admin')
        # login user
        client.login(username='admin', password='admin')
        # test gettings page with unexisted request
        response_2 = client.get(reverse('task:request_detail',
                                        args=(2, )))
        self.assertEqual(response_2.status_code, 200)


class FormProfileTests(TestCase):

    def test_profile_form(self):
        # initial data to from
        form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=form_data)
        self.assertTrue(self.form.is_valid())


class FormProfileFailedTests(TestCase):

    def tearDown(self):
        self.form = ProfileForm(data=self.form_data)
        self.assertFalse(self.form.is_valid())

    def test_profile_form_name_field(self):
        # initial data to from with fails
        # name max length
        self.form_data = {
            'id': 1,
            'name': 'admin' * 21,  # max length 100 symbols
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)
        # test if form valid
        self.assertFalse(self.form.is_valid())

        # initial data to from with fails
        # name min length
        self.form_data = {
            'id': 1,
            'name': 'ad',  # min length 3 symbols
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)

        # initial data to from with blank name
        self.form_data = {
            'id': 1,
            'name': '',  # required field
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }

    def test_profile_form_last_name_field(self):
        # initial data to from with fails
        # last_name max length
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin' * 21,  # max length 100 symbols
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)

        # initial data to from with fails
        # last_name min length
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'ad',  # min length 3 symbols
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)
        # test if form valid
        self.assertFalse(self.form.is_valid())

        # initial data to from with blank last_name
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': '',  # required field
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }

    def test_profile_form_date_of_birth_field(self):
        # initial data to from with fails
        # date format
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-29-11',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)
        # test if form valid
        self.assertFalse(self.form.is_valid())

        # initial data to from with blank
        # date of birth
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '',  # required field
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }

    def test_profile_form_email_field(self):
        # initial data to from with fails
        # email max length
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail' * 25 + '@mail.ua',  # max length 100 symbols
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)
        # test if form valid
        self.assertFalse(self.form.is_valid())

        # initial data to from with not valid
        # email address
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'ad',
            'date_of_birth': '1993-11-29',
            'email': 'mail',  # not valid email
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)
        # test if form valid
        self.assertFalse(self.form.is_valid())

        # initial data to from with blank
        # email address
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'ad',
            'date_of_birth': '1993-11-29',
            'email': '',  # required field
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
        }

    def test_profile_form_jabber_field(self):
        # initial data to from with fails
        # jabber max length
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber' * 20 + '@jabber.ua',  # max length 100 symbols
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)
        # test if form valid
        self.assertFalse(self.form.is_valid())

        # initial data to from with fails jabber input
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber',  # required email type
            'skype': 'skype',
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)
        # test if form valid
        self.assertFalse(self.form.is_valid())

        # initial data to from with blank
        # jabber field
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'ad',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': '',   # required
            'skype': 'skype',
        }

    def test_profile_form_skype_field(self):
        # initial data to from with fails
        # skype max length
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype' * 21,  # max length 100 symbols
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)
        # test if form valid
        self.assertFalse(self.form.is_valid())

        # initial data to from with fails
        # skype min length
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'sk',  # min length 3 symbols
        }
        # set initial data to from
        self.form = ProfileForm(data=self.form_data)

        # initial data to from with blank name
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': '',  # required field
        }

    def test_profile_form_other_contacts_field(self):
        # initial data to from with fails
        # other_contacts max length
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
            'other_contacts': 'testword12' * 101  # max length 1000 symbols
        }

    def test_profile_form_bio_field(self):
        # initial data to from with fails
        # bio max length
        self.form_data = {
            'id': 1,
            'name': 'admin',
            'last_name': 'admin',
            'date_of_birth': '1993-11-29',
            'email': 'mail@mail.ua',
            'jabber': 'jabber@jabber.ua',
            'skype': 'skype',
            'bio': 'testword12' * 101  # max length 1000 symbols
        }
