from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
                       url(r'^$', views.main, name='index'),
                       url(r'^edit_profile/$', views.edit_profile,
                           name='edit_profile'),
                       url(r'^request_list/$', views.request_list,
                           name='request_list'),
                       url(r'^request_list_ajax/$', views.request_list_ajax,
                           name='request_list_ajax'),
                       url(r'^request_detail/(?P<identify>[0-9]+)/$',
                           views.request_detail,
                           name='request_detail'),
                       url(r'^login/$', views.login_view, name='login'),
                       url(r'^logout/$', views.logout_view,
                           name='logout'),
                       url(r'^update_profile/$', views.update_profile,
                           name='update_profile'),
                       )