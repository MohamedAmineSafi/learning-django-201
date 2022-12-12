# from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.models import User

# Create your views here.
class ProfileDetailView(DetailView):
    http_method_names = ['get']
    template_name = "profiles/detail.html"
    model = User
    context_object_name = 'user' #default is 'object' so instead of {{object.text}} use {{user.text}}
    slug_field = 'username'
    slug_url_kwarg = 'username' #from urls.py