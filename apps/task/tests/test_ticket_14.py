# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from apps.task.forms import TaskForm
from apps.task.models import Task

client = Client()


class TasksEnterPagesTest(TestCase):
    fixtures = ['initial_data.json']

    def test_task_list_page_not_login_user(self):
        """
        Enter task page not login user
        """
        # get tasks list page
        response = self.client.get(reverse('task:tasks'))
        self.assertEqual(response.status_code, 302)

    def test_task_list_page_with_login_user(self):
        """
        Login and get /tasks/
        """
        # log in
        self.client.login(username='admin', password='admin')
        # get tasks list page
        response = self.client.get(reverse('task:tasks'))
        self.assertEqual(response.status_code, 200)

    def test_edit_task_function_login_required(self):
        """
        get edit_tasks not login user
        """
        response = self.client.post(reverse('task:edit_task'), {'id': 1})
        self.assertEqual(response.status_code, 302)

    def test_edit_task_function(self):
        """
        get edit_tasks not login user
        """
        # log in
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('task:edit_task'), {'id': 1})
        # if not valid post data return 302 to task list with error message
        self.assertEqual(response.status_code, 302)

    def test_required_method_post(self):
        """
        get edit_tasks not login user
        """
        # log in
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('task:edit_task'))
        # test method not allowed
        self.assertEqual(response.status_code, 405)

    def test_update_priority_entering_not_login_user(self):
        """
        Enter update priority with not login user
        """
        response = self.client.get(reverse('task:update_priority'))
        # get 302 to login
        self.assertEqual(response.status_code, 302)

    def test_update_priority_entering(self):
        """
        Enter update priority with login user
        """
        # log in
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('task:update_priority'))
        self.assertEqual(response.status_code, 200)


class TasksFormTest(TestCase):
    fixtures = ['initial_data.json']

    def test_valid_task_create_form(self):
        """
        Create task
        """
        form_data = {
            'user': 1,
            'title': "Title",
            'description': "Description",
            'status': 1
        }
        form = TaskForm(data=form_data)
        # test if form is not valid
        self.assertTrue(form.is_valid())

    def test_task_create_form_no_data(self):
        """
        TaskForm test send no data
        """
        form_data = {}
        form = TaskForm(data=form_data)
        # test if form is not valid
        self.assertFalse(form.is_valid())
        self.assertIn(u'This field is required',
                      str(form['user'].errors))
        self.assertIn(u'This field is required',
                      str(form['title'].errors))
        self.assertIn(u'This field is required',
                      str(form['description'].errors))
        self.assertIn(u'This field is required',
                      str(form['status'].errors))

    def test_task_create_form_not_valid_data(self):
        """
        TaskForm test send not valid data
        """
        # get tasks list page
        form_data = {
            'user': " ",
            'title': "T",
            'description': "De",
            'status': " "
        }
        form = TaskForm(data=form_data)
        # test if form is not valid
        self.assertFalse(form.is_valid())
        self.assertIn(u'Select a valid choice. '
                      u'That choice is not one of the available choices.',
                      str(form['user'].errors))
        self.assertIn(u'Ensure this value has at'
                      u' least 3 characters (it has 1).',
                      str(form['title'].errors))
        self.assertIn(u'Ensure this value has at'
                      u' least 3 characters (it has 2)',
                      str(form['description'].errors))
        self.assertIn(u'Select a valid choice.   '
                      u'is not one of the available choices.',
                      str(form['status'].errors))


class TasksTemplateAndContextTest(TestCase):
    fixtures = ['initial_data.json']

    def test_task_list_context(self):
        """
        Enter task page not login user
        """
        # log in
        self.client.login(username='admin', password='admin')
        # get tasks list page
        response = self.client.get(reverse('task:tasks'))
        # test form instance
        self.assertTrue(isinstance(response.context['form'],
                                   TaskForm))
        # test
        self.assertIn(Task.objects.filter(user_id=1).first(),
                      response.context['task'])
        # test context template
        self.assertEqual(response.context['page_template'],
                         'task/entry_tasks.html')

    def test_task_template(self):
        # log in
        self.client.login(username='admin', password='admin')
        # get tasks list page
        response = self.client.get(reverse('task:tasks'))
        self.assertIn('<form id="create_task_form"', response.content)
        self.assertIn('Create Task', response.content)
        # test russian simbols on the page
        self.assertIn('Выполнено', response.content)

    def test_task_list_post_method(self):
        # log in
        self.client.login(username='admin', password='admin')
        # get tasks list page
        response = self.client.post(reverse('task:tasks'), {
            'user': 1,
            'title': "Title",
            'description': "Description",
            'status': 1
        })
        self.assertIn('Task has been created!', response.content)
