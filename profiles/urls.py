from django.urls import path

from . import views
from .views import ProfileDetailView, FollowView, EditProfileView
app_name="profiles"

urlpatterns = [
      path("<str:username>/", views.ProfileDetailView.as_view(), name="detail"),
      path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
      path("edit/", EditProfileView.as_view(), name="edit"),
      path('profiles/', include('profiles.urls', namespace='profiles')),

]