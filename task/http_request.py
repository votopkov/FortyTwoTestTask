# -*- coding: utf-8 -* -
from models import Requests
from django.utils import timezone

class SaveHttpRequestMiddleware(object):

    def process_request(self, request):
        if request.is_ajax():
            pass
        else:
            save_request = Requests(request=request, pub_date=
            timezone.now() + timezone.timedelta(hours=3),
                                    path=request.build_absolute_uri())
            return save_request.save()
