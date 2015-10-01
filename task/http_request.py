# -*- coding: utf-8 -* -
from models import Requests


class SaveHttpRequestMiddleware(object):

    def process_request(self, request):
        if request.is_ajax():
            pass
        else:
            save_request = Requests(request=request, path=request.build_absolute_uri())
            return save_request.save()
