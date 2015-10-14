from django import forms
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings

class AdminDateWidget(forms.TextInput):
    class Media:
        js = (settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
              settings.ADMIN_MEDIA_PREFIX + "js/admin/DateTimeShortcuts.js")

    def __init__(self, attrs={}):
        attrs.update({'class': 'vDateField',
                      'size': '10',
                      'onfocus': 'javascript:DateTimeShortcuts.openCalendar(0);',
                      'onclick' : 'javascript:DateTimeShortcuts.openCalendar(0);'
                      })
        super(AdminDateWidget, self).__init__(attrs=attrs)
