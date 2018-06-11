# auth/views.py

import os
from functools import reduce
from django.core import exceptions
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



class login(LoginRequiredMixin, View):
    login_url = 'admin/'
    redirect_field_name = 'redirect_to'


class homepage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"

    def get(self, request):
        return Response(template_name=self.template_name)

class aboutpage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "about.html"

    def get(self, request):
        return Response(template_name=self.template_name)


def public(request):
    return HttpResponse("Welcome to PUBLIC Page")


@login_required
def private(request):
    return HttpResponse("Welcome to Private Page")
