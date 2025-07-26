from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest

from feed.models import Post
from followers.models import Follower

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, FollowView, homepage

# Home page listing all users
def homepage(request):
    users = User.objects.all()
    return render(request, 'profiles/home.html', {'users': users})


# Edit Profile View (Function-Based View)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profiles:detail', username=request.user.username)  # Fix redirect target
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


# Profile Detail Page
class ProfileDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()

        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(
                following=user,
                followed_by=self.request.user,
            ).exists()
        else:
            context['you_follow'] = False

        return context


# AJAX Follow / Unfollow View
class FollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")

        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("User not found")

        if data['action'] == "follow":
            Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
            wording = "Unfollow"
        else:
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following=other_user
                )
                follower.delete()
            except Follower.DoesNotExist:
                pass
            wording = "Follow"

        return JsonResponse({
            'success': True,
            'wording': wording
        })
