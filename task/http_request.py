# -*- coding: utf-8 -* -
from models import Requests


class SaveHttpRequestMiddleware(object):

    def process_request(self, request):
        save_request = Requests(request=request)
        return save_request.save()
