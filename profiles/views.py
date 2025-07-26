from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.forms import UserChangeForm  # ✅ Use built-in form

from feed.models import Post
from followers.models import Follower

# ✅ Homepage View — show all users
def homepage(request):
    users = User.objects.all()
    return render(request, "profiles/home.html", {"users": users})

# ✅ Edit Profile View — no custom form needed
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm  # ✅ Using built-in form instead of missing EditProfileForm
    template_name = 'profiles/edit_profile.html'
    success_url = reverse_lazy('profiles:home')

    def get_object(self):
        return self.request.user

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
