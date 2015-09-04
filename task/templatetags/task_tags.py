# -*- coding: utf-8 -*-
from django import template
from django.core import urlresolvers

register = template.Library()


@register.simple_tag
def get_edit_admin_page(profile_id):
    url_to_admin_edit_page = urlresolvers.reverse('admin:task_profile_change',
                                                  args=(profile_id,))
    return url_to_admin_edit_page
