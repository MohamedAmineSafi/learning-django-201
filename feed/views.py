# from django.shortcuts import render NOT USING FUNCTION BASED VIEW
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Post
from followers.models import Follower

# Create your views here.
class HomePage(TemplateView):
    http_method_names = ['get']
    template_name = 'feed/homepage.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            following = list( Follower.objects.filter(followed_by=self.request.user).values_list('following', flat=True) )
            if not following:
                posts = Post.objects.all().order_by("-id")[0:30] #first 30
            else:
                posts = Post.objects.filter(author__in=following).order_by('-id')[0:60]
        
        else:
            posts = Post.objects.all().order_by("-id")[0:30] #first 30
        
        context['posts'] = posts
        return context

class PostDetailView(DetailView):
    http_method_names = ['get']
    template_name = "feed/detail.html"
    model = Post
    context_object_name = 'post' #default is 'object' so instead of {{object.text}} use {{post.text}}

class CreateNewPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "feed/create.html"
    fields = ['text']
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False) #DO NOT SAVE THE FORM like 'PreventDefault' in jQuery
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            text = request.POST.get("text"),
            author = request.user
        )

        return render( #This is the response sent back to jQuery (set in the var 'dataHtml')
            request,
            'includes/post.html',
            {
                "post": post,
                "show_detail_link": True,
            },
            content_type = "application/html",
        )