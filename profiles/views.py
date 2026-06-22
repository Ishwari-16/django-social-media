from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q

from feed.models import Post
from followers.models import Follower
from .models import Profile
from .forms import EditProfileForm  # ✅ Make sure this exists

# ✅ Homepage View
def homepage(request):
    return render(request, 'profiles/home.html')

# ✅ Edit Profile (Class-Based)
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

class EditProfileView(View):
    def get(self, request):
        return render(request, 'profiles/edit_profile.html')

    def post(self, request):
        user = request.user

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')

        password = request.POST.get('password')
        if password:
            user.set_password(password)

        # For image upload
        if 'profile_image' in request.FILES:
            user.profile.profile_image = request.FILES['profile_image']
            user.profile.save()

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profiles:edit')  # Or wherever you want to redirect

def edit_name_username(request):
    return render(request, 'profiles/edit_name_username.html')

# ✅ Edit Profile Image View
class EditProfileImageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profiles/edit_image.html')

    def post(self, request):
        profile = request.user.profile
        profile.profile_image = request.FILES.get('image')
        profile.save()
        return redirect('profiles:detail', username=request.user.username)


# ✅ Edit Cover Photo View
class EditCoverPhotoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profiles/edit_cover.html')

    def post(self, request):
        profile = request.user.profile
        profile.cover_photo = request.FILES.get('cover_photo')
        profile.save()
        return redirect('profiles:detail', username=request.user.username)

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

        context['you_follow'] = False
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(
                following=user,
                followed_by=self.request.user,
            ).exists()

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
        
        print("ACTION =", data['action'])
        print("USER =", data['username'])

        if data['action'] == "follow":
            Follower.objects.get_or_create(followed_by=request.user, following=other_user)
            wording = "Unfollow"
        else:
            Follower.objects.filter(followed_by=request.user, following=other_user).delete()
            wording = "Follow"

        return JsonResponse({'success': True, 'wording': wording})

# ✅ Search View
def search(request):
    query = request.GET.get('q', '')
    
    users = []
    posts = []
    
    if query:
        # Search users by username, first name, last name
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).distinct()
        
        # Search posts by content
        posts = Post.objects.filter(
            Q(text__icontains=query)
        ).order_by('-id')[:20]
    
    return render(request, 'profiles/search_results.html', {
        'query': query,
        'users': users,
        'posts': posts,
    })
