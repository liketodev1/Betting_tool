import json
from django.http import HttpResponse
from django.shortcuts import render
from frontend.models import Scores
from .serializers import FrontSerializer
from rest_framework.generics import ListAPIView
import os
from django.conf import settings



class FrontListView(ListAPIView):

    queryset = Scores.objects.all()
    serializer_class = FrontSerializer

    def get(self, request):
        result = open(os.path.join(settings.BASE_DIR, 'result')).read()
        data = {'res': result}
        return HttpResponse(json.dumps({'status': 'ok', 'data': result,}), status=200, content_type='application/json')
