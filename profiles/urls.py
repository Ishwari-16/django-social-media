from django.urls import path

from . import views
from .views import ProfileDetailView, FollowView, EditProfileView
from django.urls import path, include

app_name="profiles"

urlpatterns = [
      path("<str:username>/", views.ProfileDetailView.as_view(), name="detail"),
      path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
      path('edit/', views.edit_profile, name='edit'),
      path('profiles/', include('profiles.urls', namespace='profiles')),

]