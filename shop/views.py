from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View

class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, World!")