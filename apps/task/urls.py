from django.conf.urls import patterns, url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = patterns('',
                       url(r'^$', views.main, name='index'),
                       url(r'^edit_profile/$', views.edit_profile,
                           name='edit_profile'),
                       url(r'^request_list/$', views.request_list,
                           name='request_list'),
                       url(r'^request_list_ajax/$', views.request_list_ajax,
                           name='request_list_ajax'),
                       url(r'^login/$', auth_views.login, name='login'),
                       url(r'^logout/$', auth_views.logout, {
                           'next_page': '/'
                       }, name='logout'),
                       url(r'^update_profile/$', views.update_profile,
                           name='update_profile'),
                       url(r'^tasks/$', views.tasks, name='tasks'),
                       url(r'^edit_task$', views.edit_task, name='edit_task'),
                       url(r'^update_priority/$', views.update_priority,
                           name='update_priority'),
                       )
