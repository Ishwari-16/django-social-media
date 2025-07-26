from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest

from feed.models import Post
from followers.models import Follower

from django.views.generic.edit import UpdateView
from django.shortcuts import redirect, render
from .models import Profile
from .forms import EditProfileForm


def edit_profile(request):
    if request.method == 'POST':
        # You’ll handle form data here later
        pass
    return render(request, 'profiles/edit_profile.html')

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "profiles/edit.html"
    success_url = "/"

    def get_object(self):
        return self.request.user

class ProfileDetailView(DetailView):
      http_method_names=["get"]
      template_name="profiles/detail.html"
      model=User
      context_object_name="user"
      slug_field="username"
      slug_url_kwarg="username"

      def dispatch(self,request,*args,**kwargs):
            self.request=request
            return super().dispatch(request,*args,**kwargs)

      def get_context_data(self,**kwargs):
            user=self.get_object()
            context=super().get_context_data(**kwargs)
            context['total_posts']=Post.objects.filter(author=user).count()
            
            if self.request.user.is_authenticated:
                context['you_follow'] = Follower.objects.filter(
                  following = user,
                  followed_by = self.request.user,
                ).exists()
            else:
                context['you_follow'] = False

            return context


class FollowView(LoginRequiredMixin, View):
      http_method_names=["post"]

      def post(self,request,*args,**kwargs):
            data = request.POST.dict()

            if "action" not in data or "username" not in data:
                  return HttpResponseBadRequest("Missing data")

            try:
                  other_user=User.objects.get(username=data['username'])
            except User.DoesNotExist:
                  return HttpResponseBadRequest("Missing user")
  
            if data['action'] == "follow":
            # Follow
                  Follower.objects.get_or_create(
                        followed_by=request.user,
                        following=other_user
                  )
                  wording = "Unfollow"
            else:
            # Unfollow
                  try:
                        follower = Follower.objects.get(
                            followed_by=request.user,
                            following=other_user,
                        )
                        follower.delete()
                  except Follower.DoesNotExist:
                        pass
                  wording = "Follow"

            return JsonResponse({
                  'success': True,
                  'wording': wording
            })

                  #if data['action'] == "follow":
                        #Follow
                   #     follower,created=Follower.objects.get_or_create(
                    #          followed_by=request.user,
                     #         following=other_user
                      #  )
                 # else:
                        #Unfollow
                  #      try:
                   #           follower=Follower.objects.get(
                    #                followed_by=request.user,
                     #               following=other_user,
                      #        )
                       # except Follower.DoesNotExist:
                        #      follower=None
                        
                       # if follower:
                        #      follower.delete()

              #    return JsonResponse({
               #         'success':True,
                #        'wording':wording
                 #       #'wording':"Unfollow" if data['action']=="follow" else "Follow"
                  #})'''


      #def post(self,request,*args,**kwargs):
       #     return JsonResponse({
        #          data == request.POST.dict(),
         #         'done':True
          #  })
