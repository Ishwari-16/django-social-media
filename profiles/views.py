from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from feed.models import Post
from followers.models import Follower
from .models import Profile

# ✅ Homepage View
def homepage(request):
    return render(request, 'profiles/home.html')

# ✅ Edit Profile View (Function-Based View)

def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user=user, data=request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)

            if 'profile_image' in request.FILES:
                profile.image = request.FILES['profile_image']
                profile.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles:edit_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = EditProfileForm(instance=user)
        password_form = PasswordChangeForm(user=user)

    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })

# ✅ Edit Profile Image View (Optional)
class EditProfileImageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profiles/edit_image.html')

    def post(self, request):
        profile = request.user.profile
        profile.image = request.FILES.get('image')
        profile.save()
        return redirect('profiles:profile', username=request.user.username)

# ✅ Profile Detail Page View
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
        context['followers_count'] = Follower.objects.filter(following=user).count()
        context['following_count'] = Follower.objects.filter(followed_by=user).count()

        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(
                following=user,
                followed_by=self.request.user,
            ).exists()
        else:
            context['you_follow'] = False

        return context

# ✅ Follow/Unfollow AJAX View
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
