# from django.shortcuts import render
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest

from feed.models import Post
from followers.models import Follower

# Create your views here.
class ProfileDetailView(DetailView):
    http_method_names = ['get']
    template_name = "profiles/detail.html"
    model = User
    context_object_name = 'user' #default is 'object' so instead of {{object.text}} use {{user.text}}
    slug_field = 'username'
    slug_url_kwarg = 'username' #from urls.py

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        return context

class FollowView(LoginRequiredMixin, View):
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing Data")
        
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing User")

        if data['action'] == 'follow':
            follower, created = Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following=other_user
                )
            except Follower.DoesNotExist:
                follower = None
            
            if follower:
                follower.delete()

        return JsonResponse({
            'success': True,
            'wording': "Unfollow" if data['action'] == 'follow' else "Follow"
        })