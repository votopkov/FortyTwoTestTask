# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from models import Profile, Requests
from django.conf import settings
from http_request import SaveHttpRequestMiddleware
from forms import ProfileForm, LoginForm
from django.utils.six import StringIO
from django.template import Template, Context
from task.templatetags.task_tags import get_edit_admin_page


client = Client()


class ProfileMethodTests(TestCase):

    def setUp(self):
        Profile.objects.create(name=u"Владимир", last_name=u"Отопков")
        Profile.objects.create(name=u"Василий", last_name=u"Петров")
        User.objects.create_user('admin', ' ', 'admin')

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
        # test if not another profile on the main page
        self.assertNotIn('Василий', response.content)

    def test_main_page_login_in_user(self):
        """
        Testing profile update form
        """
        self.client.login(username='admin', password='admin')
        # get page
        response = self.client.get(reverse('task:index'))
        # if index page exists
        self.assertEqual(response.status_code, 200)
        # test form exist
        self.assertContains(response, 'Save')

    def test_command_output(self):
        out = StringIO()
        call_command('model_list', stdout=out)
        self.assertIn('task.models.Requests', out.getvalue())

    def test_tag(self):
        self.profile = Profile.objects.get(id=settings.DEFAULT_PROFILE_ID)
        self.template = Template("{% load task_tags %}"
                                 " {% get_edit_admin_page profile.id %}")
        rendered = self.template.render(Context({'profile': self.profile}))
        self.assertIn(get_edit_admin_page(settings.DEFAULT_PROFILE_ID),
                      rendered)

    def test_signals(self):
        pass


class SaveHttpRequestTests(TestCase):

    def setUp(self):
        Requests.objects.create(request='request_1')
        Requests.objects.create(request='request_2')
        User.objects.create_user('admin', ' ', 'admin')

    def test_request_list(self):
        """
        Testing request list view function
        """
        # get requests
        client.login(username='admin', password='admin')
        response = client.get(reverse('task:request_list'),
                              content_type='application/json',
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # not login user
        client_2 = Client()
        response_2 = client_2.get(reverse('task:request_list'),
                                  content_type='application/json',
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response_2.status_code, 302)
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
        self.new_request = Client()
        self.new_request.login(username='admin', password='admin')
        # save request to DB
        self.save_http.process_request(request=self.new_request)
        # test saving request to DB
        self.assertEqual(Requests.objects.all().count(), 3)


class FormTests(TestCase):

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
        # initial data to form (not valid)
        failed_form_data = {
            'id': 2,
            'name': 'name',
            'last_name': 'last_name'
        }
        # set initial data to from
        form = ProfileForm(data=form_data)
        # set failed data to form
        failed_form = ProfileForm(data=failed_form_data)
        # test if form valid
        self.assertTrue(form.is_valid())
        # test if form invalid
        self.assertFalse(failed_form.is_valid())

    def test_login_form(self):
        # initial data to from
        form_data = {
            'username': 'admin',
            'password': 'password'
        }
        # length is less than 3(username)
        failed_min_length = {
            'username': 'ad',
            'password': '12345'
        }
        # length is getter than 100(password)
        failed_max_length = {
            'username': 'admin' * 200,
            'password': 'assd'
        }
        # no data
        failed_no_input = {
            'username': '',
            'password': ''
        }
        # set valid initial data
        form = LoginForm(data=form_data)
        # not valid min length of username field
        form_min_length = LoginForm(data=failed_min_length)
        # not valid max length of username field
        form_max_length = LoginForm(data=failed_max_length)
        # no data in form
        form_no_data = LoginForm(data=failed_no_input)
        # test form
        self.assertTrue(form.is_valid())
        self.assertFalse(form_min_length.is_valid())
        self.assertFalse(form_max_length.is_valid())
        self.assertFalse(form_no_data.is_valid())
