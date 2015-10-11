# -*- coding: utf-8 -*-
from django_assets import Bundle, register

css = Bundle('bootstrap-3.3.5-dist/css/bootstrap.min.css', 'css/style.css',
             filters='cssmin',
             output='css_all.css')
register('all_css', css)
