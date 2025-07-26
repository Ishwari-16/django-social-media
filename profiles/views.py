from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from feed.models import Post
from followers.models import Follower
from .models import Profile
from .forms import EditProfileForm

# ✅ Homepage View — optional
def homepage(request):
    return render(request, 'profiles/home.html')

# ✅ Edit Profile View
class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = EditProfileForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        return render(request, 'profiles/edit_profile.html', {
            'user_form': user_form,
            'password_form': password_form
        })

    def profile_view(request, username):
        user = User.objects.get(username=username)
        followers_count = Follower.objects.filter(followed=user).count()

        # Add posts count too if you're using it
        posts_count = user.post_set.count()  # adjust based on your Post model name

        return render(request, 'profile.html', {
            'user': user,
            'followers_count': followers_count,
            'posts_count': posts_count,
        })

    def update_profile(request):
        if request.method == 'POST':
        # handle full profile update including image
            ...
            messages.success(request, "Profile updated successfully!")
            return redirect('update_profile')
        return render(request, 'edit_profile.html')



def edit_name_username(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.username = request.POST.get('username', '')
        user.save()
        messages.success(request, 'Name/Username updated successfully!')
        return redirect('profiles:edit_name_username')
    return render(request, 'profiles/edit_name_username.html')
    def post(self, request):
        user_form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()

            # Save profile image if included
            profile = request.user.profile
           # ✅ Correct
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
                profile.save()

            # Handle password change
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated successfully!')

            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles:edit_profile')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'profiles/edit_profile.html', {
            'user_form': user_form,
            'password_form': password_form
        })

# ✅ Image-only update (optional)
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
