# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys


class ProfileAdminTest(LiveServerTestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # Open admin page
        self.browser.get(self.live_server_url + reverse('admin:index'))

        # Test if you are in admin
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # Fill in admin enter form
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Find Profile in admin
        profile_link = self.browser.find_element_by_link_text(
            'Profiles')

        # Go to profile
        profile_link.click()

        # Find profile Otopkov
        profile = self.browser.find_element_by_link_text('Отопков')
        profile.click()

        # Editing profile last name
        last_name = self.browser.find_element_by_name('last_name')
        last_name.clear()
        last_name.send_keys("Petrov")
        save_button = self.browser.find_element_by_css_selector(
            "input[value='Save']")
        save_button.click()

        # test changing last_name
        profile = self.browser.find_element_by_link_text('Petrov')
        self.assertTrue(profile)


class RequestsAdminTest(LiveServerTestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # Open admin page
        self.browser.get(self.live_server_url + reverse('admin:index'))

        # Test if you are in admin
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # Fill in admin enter form
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Find Requests model
        request_link = self.browser.find_element_by_link_text(
            'Requestss')

        # Go to Requests model
        request_link.click()

        # Get request
        request = self.browser.find_element_by_link_text('Http_request')
        request.click()

        # Editing profile
        last_name = self.browser.find_element_by_name('priority')
        last_name.clear()
        last_name.send_keys(1)
        save_button = self.browser.find_element_by_css_selector(
            "input[value='Save']")
        save_button.click()


class SavedSignalsAdminTest(LiveServerTestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # Open admin page
        self.browser.get(self.live_server_url + reverse('admin:index'))

        # Test if you are in admin
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # She types in her username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Fill in admin enter form
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # Get link to SavedSignals model
        saved_signals_link = self.browser.find_element_by_link_text(
            'Saved signalss')

        # go to SavedSignals entry
        saved_signals_link.click()

        # find Profile
        profile = self.browser.find_element_by_link_text('Profile')
        profile.click()

        # Editing SavedSignals
        last_name = self.browser.find_element_by_name('status')
        last_name.clear()
        last_name.send_keys("updated")
        save_button = self.browser.find_element_by_css_selector(
            "input[value='Save']")
        save_button.click()
