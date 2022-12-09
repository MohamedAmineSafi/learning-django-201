# from django.shortcuts import render NOT USING FUNCTION BASED VIEW
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Post

# Create your views here.
class HomePage(ListView):
    http_method_names = ['get']
    template_name = 'feed/homepage.html'
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-id')[0:30] #Get only 30 posts

class PostDetailView(DetailView):
    http_method_names = ['get']
    template_name = "feed/detail.html"
    model = Post
    context_object_name = 'post' #default is 'object' so instead of {{object.text}} use {{post.text}}

class CreateNewPost(CreateView):
    model = Post
    template_name = "feed/create.html"
    fields = ['text']