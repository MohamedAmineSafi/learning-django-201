# from django.shortcuts import render NOT USING FUNCTION BASED VIEW
from django.views.generic import ListView
from .models import Post

# Create your views here.
class HomePage(ListView):
    http_method_names = ['get']
    template_name = 'homepage.html'
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-id')[0:30] #Get only 30 posts