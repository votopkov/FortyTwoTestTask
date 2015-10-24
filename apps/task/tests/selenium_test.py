# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys


class ProfileTest(LiveServerTestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # Go to main page
        self.browser.get(self.live_server_url)

        # Find 42 Coffee Cups Test Assignment in body
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('42 Coffee Cups Test Assignment', body.text)

        # Get login link
        login_link = self.browser.find_element_by_link_text('Login')

        # Login
        login_link.click()

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Get edit admin link
        edit_admin = self.browser.find_element_by_link_text('(admin)')
        edit_admin.click()

        # Test if you are in admin
        last_name = self.browser.find_element_by_name('last_name')
        self.assertEqual(last_name.get_attribute('value'), u'Отопков')


class ProfileEditTest(LiveServerTestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # Go to edit profile page
        self.browser.get(self.live_server_url + reverse(
            'task:edit_profile'))

        # Redirect to login
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Get edit link
        edit_admin = self.browser.find_element_by_link_text('Edit')
        edit_admin.click()

        # change name to Василий
        name = self.browser.find_element_by_name('name')
        name.clear()
        name.send_keys(u'Василий')

        save_button = self.browser.find_element_by_css_selector(
            "input[value='Save']")
        save_button.click()

        # Check update name
        name = self.browser.find_element_by_name('name')
        self.assertEqual(name.get_attribute('value'), u'Василий')

        # Get cancel link
        cancel_link = self.browser.find_element_by_link_text('Cancel')
        cancel_link.click()

        # Test if you are in main page
        logout_link = self.browser.find_element_by_link_text('Logout')
        self.assertEqual(logout_link.text, 'Logout')


class LogoutTest(LiveServerTestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # Go to main page
        self.browser.get(self.live_server_url)

        # Get login link
        login_link = self.browser.find_element_by_link_text('Login')

        # Login
        login_link.click()

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Get logout link
        logout_link = self.browser.find_element_by_link_text('Logout')
        self.assertEqual(logout_link.text, 'Logout')

        logout_link.click()

        # Test if logout is working
        # Get login link
        login_link = self.browser.find_element_by_link_text('Login')
        self.assertEqual(login_link.text, 'Login')


class RequestListTest(LiveServerTestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):

        # Go to main page
        self.browser.get(self.live_server_url)

        # Go to request list
        request_link = self.browser.find_element_by_link_text(
            'requests')
        request_link.click()

        # Test if table with requests on the page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('ID', body.text)
        self.assertIn('Date', body.text)
        self.assertIn('Path', body.text)
        self.assertIn('Priority', body.text)
